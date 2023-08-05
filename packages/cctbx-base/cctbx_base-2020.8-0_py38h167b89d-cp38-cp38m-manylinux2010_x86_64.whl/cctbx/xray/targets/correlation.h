#ifndef CCTBX_XRAY_TARGETS_CORRELATION_H
#define CCTBX_XRAY_TARGETS_CORRELATION_H

#include <cctbx/xray/targets/common_results.h>
#include <boost/scoped_array.hpp>
#include <cmath>

namespace cctbx { namespace xray { namespace targets {

  struct correlation : common_results
  {
    protected:
      char obs_type_;
      boost::optional<double> cc_;
      public:

    static double
    numeric_epsilon() { return 1e-12; }

    correlation() {}

    correlation(
      char obs_type,
      af::const_ref<double> const& obs,
      af::const_ref<double> const& weights,
      af::const_ref<bool> const& r_free_flags,
      af::const_ref<std::complex<double> > const& f_calc,
      int derivatives_depth)
    :
      common_results(obs.size()),
      obs_type_(obs_type)
    {
      TBXX_ASSERT(obs_type == 'F' || obs_type == 'I');
      TBXX_ASSERT(weights.size() == 0 || weights.size() == obs.size());
      TBXX_ASSERT(r_free_flags.size() == 0
               || r_free_flags.size() == obs.size());
      TBXX_ASSERT(f_calc.size() == obs.size());
      TBXX_ASSERT(derivatives_depth >= 0 && derivatives_depth <= 2);
      const double* wghts = weights.begin();
      const bool* rff = r_free_flags.begin();
      std::size_t n_work = 0;
      double sum_w = 0;
      double sum_wx = 0;
      double sum_wy = 0;
      boost::scoped_array<double> wb(new double[obs.size()]);
      boost::scoped_array<double> xb(new double[obs.size()]);
      boost::scoped_array<double> yb(new double[obs.size()]);
      double w = 1;
      for(std::size_t i=0;i<obs.size();i++) {
        if (rff == 0 || !rff[i]) {
          if (wghts != 0) {
            w = wghts[i];
            sum_w += wghts[i];
          }
          double x = obs[i];
          double y = (obs_type == 'F'
            ? std::abs(f_calc[i])
            : std::norm(f_calc[i]));
          sum_wx += w * x;
          sum_wy += w * y;
          wb[n_work] = w;
          xb[n_work] = x;
          yb[n_work] = y;
          n_work++;
        }
      }
      if (wghts == 0) sum_w = static_cast<double>(n_work);
      if (sum_w <= 0) {
        return;
      }
      double wxm = sum_wx / sum_w;
      double wym = sum_wy / sum_w;
      double sum_wxy = 0;
      double sum_wxx = 0;
      double sum_wyy = 0;
      {
        double min_x = xb[0];
        double max_x = min_x;
        double min_y = yb[0];
        double max_y = min_y;
        for(std::size_t i_work=0;i_work<n_work;i_work++) {
          double w = wb[i_work];
          double& xc = xb[i_work];
          double& yc = yb[i_work];
          if (min_x > xc) min_x = xc;
          if (max_x < xc) max_x = xc;
          if (min_y > yc) min_y = yc;
          if (max_y < yc) max_y = yc;
          xc -= wxm;
          yc -= wym;
          sum_wxy += w * xc * yc;
          sum_wxx += w * xc * xc;
          sum_wyy += w * yc * yc;
        }
        double range_x = max_x - min_x;
        if (min_x < 0) min_x *= -1;
        if (max_x < 0) max_x *= -1;
        if (max_x < min_x) max_x = min_x;
        if (range_x <= max_x * numeric_epsilon()) {
          return;
        }
        double range_y = max_y - min_y;
        if (min_y < 0) min_y *= -1;
        if (max_y < 0) max_y *= -1;
        if (max_y < min_y) max_y = min_y;
        if (range_y <= max_y * numeric_epsilon()) {
          return;
        }
      }
      double cc_den_sq = sum_wxx * sum_wyy;
      double cc_den_qu = cc_den_sq * cc_den_sq;
      if (cc_den_qu == 0) {
        return;
      }
      double cc_den = std::sqrt(cc_den_sq);
      TBXX_ASSERT(cc_den != 0);
      double cc = sum_wxy / cc_den;
      if      (cc >  1) cc =  1; // compensate for rounding errors
      else if (cc < -1) cc = -1;
      cc_ = cc;
      target_work_ = 1 - cc;
      if (derivatives_depth != 0) {
        gradients_work_.reserve(n_work);
        if (derivatives_depth == 2) {
          hessians_work_.reserve(n_work);
        }
        std::size_t i_work = 0;
        for(std::size_t i=0;i<obs.size();i++) {
          if (rff == 0 || !rff[i]) {
            double w = wb[i_work];
            double xc = xb[i_work];
            double yc = yb[i_work];
            i_work++;
            double d_sum_wxy = w * xc;
            double d_sum_wyy = 2 * w * yc;
            double d_cc_den_sq = sum_wxx * d_sum_wyy;
            double d_cc_den = 1 / (2 * cc_den) * d_cc_den_sq;
            double d_cc_num = d_sum_wxy * cc_den - sum_wxy * d_cc_den;
            double d_cc = d_cc_num / cc_den_sq;
            //
            double a = f_calc[i].real();
            double b = f_calc[i].imag();
            double y = 0;
            double y3 = 0;
            double gf = 0;
            if (obs_type == 'F') {
              y = std::sqrt(a*a + b*b);
              y3 = y * y * y;
              if (y3 != 0) gf = d_cc / y;
            }
            else {
              gf = 2 * d_cc;
            }
            gradients_work_.push_back(std::complex<double>(-gf*a, -gf*b));
            if (derivatives_depth == 2) {
              double d_yc = 1 - w / sum_w;
              double d2_sum_wyy = 2 * w * d_yc;
              double d2_cc_den_sq = sum_wxx * d2_sum_wyy;
              double d2_cc_den = 0.5 * (d2_cc_den_sq / cc_den
                - d_cc_den_sq * d_cc_den / cc_den_sq);
              double d2_cc_num = -sum_wxy * d2_cc_den;
              double d2_cc = d2_cc_num / cc_den_sq
                - d_cc_num * d_cc_den_sq / cc_den_qu;
              scitbx::vec3<double> cw;
              if (obs_type == 'F') {
                if (y3 == 0) {
                  cw.fill(1);
                }
                else {
                  TBXX_ASSERT(y != 0);
                  double dya = a / y;
                  double dyb = b / y;
                  double d2yaa = b*b / y3;
                  double d2ybb = a*a / y3;
                  double d2yab = -a*b / y3;
                  /*daa*/ cw[0] = -(d2_cc * dya * dya + d_cc * d2yaa);
                  /*dbb*/ cw[1] = -(d2_cc * dyb * dyb + d_cc * d2ybb);
                  /*dab*/ cw[2] = -(d2_cc * dyb * dya + d_cc * d2yab);
                }
              }
              else {
                /*daa*/ cw[0] = -(d2_cc * 4 * a * a + d_cc * 2);
                /*dbb*/ cw[1] = -(d2_cc * 4 * b * b + d_cc * 2);
                /*dab*/ cw[2] = -(d2_cc * 4 * a * b);
              }
              hessians_work_.push_back(cw);
            }
          }
        }
      }
    }

    char
    obs_type() const { return obs_type_; }

    boost::optional<double>
    cc() const { return cc_; }
  };

}}} // namespace cctbx::xray::targets

#endif // GUARD
