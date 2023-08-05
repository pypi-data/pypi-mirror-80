#ifndef CCTBX_MILLER_MERGE_EQUIVALENTS_H
#define CCTBX_MILLER_MERGE_EQUIVALENTS_H

#include <boost/optional.hpp>

#include <cctbx/sgtbx/space_group.h>
#include <scitbx/math/mean_and_variance.h>
#include <scitbx/math/linear_regression.h>
#include <scitbx/random.h>

namespace cctbx { namespace miller {

  template <typename DataElementType>
  struct merge_equivalents_impl
  {
    template <typename DerivedType>
    void
    loop_over_groups(
      DerivedType& self,
      af::const_ref<index<> > const& unmerged_indices,
      af::const_ref<DataElementType> const& unmerged_data)
    {
      CCTBX_ASSERT(unmerged_data.size() == unmerged_indices.size());
      if (unmerged_indices.size() == 0) return;
      std::size_t group_begin = 0;
      std::size_t group_end = 1;
      for(;group_end<unmerged_indices.size();group_end++) {
        if (unmerged_indices[group_end] != unmerged_indices[group_begin]) {
          process_group(
            self, group_begin, group_end,
            unmerged_indices[group_begin], unmerged_data);
          group_begin = group_end;
        }
      }
      process_group(
        self, group_begin, group_end,
        unmerged_indices[group_begin], unmerged_data);
    }

    template <typename DerivedType>
    void
    process_group(
      DerivedType& self,
      std::size_t group_begin,
      std::size_t group_end,
      index<> const& current_index,
      af::const_ref<DataElementType> const& unmerged_data)
    {
      std::size_t n = group_end - group_begin;
      if (n == 0) return;
      self.indices.push_back(current_index);
      self.data.push_back(self.merge(
        current_index, &unmerged_data[group_begin], n));
      self.redundancies.push_back(n);
    }
  };

  namespace merge_equivalents {

    template <
      typename DerivedType,
      typename DataElementType,
      typename FloatType>
    void
    compute_r_factors(
      DerivedType& self,
      const DataElementType* data_group,
      std::size_t n,
      FloatType const& result)
    {
      FloatType sum_num = scitbx::fn::absolute(data_group[0] - result);
      FloatType sum_den = scitbx::fn::absolute(data_group[0]);
      FloatType sum_merge_den = data_group[0];
      for(std::size_t i=1;i<n;i++) {
        sum_num += scitbx::fn::absolute(data_group[i] - result);
        sum_den += scitbx::fn::absolute(data_group[i]);
        sum_merge_den += data_group[i];
      }
      if (sum_den == 0) self.r_linear.push_back(0);
      else self.r_linear.push_back(sum_num / sum_den);
      if (n != 1) {
        self.r_int_num += sum_num;
        self.r_int_den += sum_den;
        self.r_merge_den += sum_merge_den;
        self.r_meas_num += std::sqrt((FloatType)n/(FloatType)(n-1)) * sum_num;
        self.r_pim_num += std::sqrt(1.0 / (FloatType)(n-1)) * sum_num;
      }
      //
      sum_num = scitbx::fn::pow2(data_group[0] - result);
      sum_den = scitbx::fn::pow2(data_group[0]);
      for(std::size_t i=1;i<n;i++) {
        sum_num += scitbx::fn::pow2(data_group[i] - result);
        sum_den += scitbx::fn::pow2(data_group[i]);
      }
      if (sum_den == 0) self.r_square.push_back(0);
      else self.r_square.push_back(sum_num / sum_den);
    }

  } // namespace merge_equivalents

  template <typename StringElementType, typename FloatType>
  struct merge_equivalents_string : merge_equivalents_impl<StringElementType>
  {
    merge_equivalents_string() {}

    merge_equivalents_string(
      af::const_ref<index<> > const& unmerged_indices,
      af::const_ref<StringElementType> const& unmerged_data)
    {
      merge_equivalents_impl<StringElementType>
        ::loop_over_groups(*this, unmerged_indices, unmerged_data);
    }

    af::shared<index<> > indices;
    af::shared<StringElementType> data;
    af::shared<int> redundancies;

    StringElementType
      merge(
        miller::index<> const& /*current_index*/,
        const StringElementType* data_group, std::size_t n)
    {
      StringElementType result = data_group[0];
      for (std::size_t i = 1; i < n; i++) result += "\n" + data_group[i];
      return result;
    }
  };

  template <typename DataElementType, typename FloatType>
  struct merge_equivalents_generic : merge_equivalents_impl<DataElementType>
  {
    merge_equivalents_generic() {}

    merge_equivalents_generic(
      af::const_ref<index<> > const& unmerged_indices,
      af::const_ref<DataElementType> const& unmerged_data)
    {
      merge_equivalents_impl<DataElementType>
        ::loop_over_groups(*this, unmerged_indices, unmerged_data);
    }

    af::shared<index<> > indices;
    af::shared<DataElementType> data;
    af::shared<int> redundancies;

    DataElementType
      merge(
        miller::index<> const& /*current_index*/,
        const DataElementType* data_group, std::size_t n)
    {
      DataElementType result = data_group[0];
      for (std::size_t i = 1; i < n; i++) result += data_group[i];
      return result / static_cast<FloatType>(n);
    }
  };

  template <typename IntegralType>
  struct merge_equivalents_exact : merge_equivalents_impl<IntegralType>
  {
    merge_equivalents_exact() {}

    merge_equivalents_exact(
      af::const_ref<index<> > const& unmerged_indices,
      af::const_ref<IntegralType> const& unmerged_data,
      boost::optional<IntegralType> incompatible_flags_replacement=boost::optional<IntegralType>())
    :
      incompatible_flags_replacement(incompatible_flags_replacement),
      n_incompatible_flags(0)
    {
      merge_equivalents_impl<IntegralType>
        ::loop_over_groups(*this, unmerged_indices, unmerged_data);
    }

    af::shared<index<> > indices;
    af::shared<IntegralType> data;
    af::shared<int> redundancies;
    boost::optional<IntegralType> incompatible_flags_replacement;
    int n_incompatible_flags;

    IntegralType
    merge(
      miller::index<> const& current_index,
      const IntegralType* data_group, std::size_t n)
    {
      for(std::size_t i=1;i<n;i++) {
        if (data_group[i] != data_group[0]) {
          if (incompatible_flags_replacement) {
            n_incompatible_flags++;
            return *incompatible_flags_replacement;
          }
          char buf[128];
          std::sprintf(buf,
            "merge_equivalents_exact:"
            " incompatible flags for hkl = (%d, %d, %d)",
            current_index[0], current_index[1], current_index[2]);
          throw error(buf);
        }
      }
      return data_group[0];
    }
  };

  template <typename FloatType=double>
  struct merge_equivalents_real : merge_equivalents_impl<FloatType>
  {
    merge_equivalents_real()
      : r_int_num(0), r_int_den(0), r_merge_den(0), r_meas_num(0), r_pim_num(0)
    {}

    merge_equivalents_real(
      af::const_ref<index<> > const& unmerged_indices,
      af::const_ref<FloatType> const& unmerged_data)
    : r_int_num(0), r_int_den(0), r_merge_den(0), r_meas_num(0), r_pim_num(0)
    {
      merge_equivalents_impl<FloatType>
        ::loop_over_groups(*this, unmerged_indices, unmerged_data);
    }

    af::shared<index<> > indices;
    af::shared<FloatType> data;
    af::shared<int> redundancies;
    //! r_linear = sum(abs(data - mean(data))) / sum(abs(data))
    af::shared<FloatType> r_linear;
    //! r_square = sum((data - mean(data))**2) / sum(data**2)
    af::shared<FloatType> r_square;
    /** r_int = sum(abs(data - mean(data))) / sum(abs(data))
    where the sums run over all unique reflections but mean(data) is the
    same as for r_linear, i.e. the mean for the group of symmetry
    equivalent reflections.
    */
    FloatType r_int_num, r_int_den;
    // r_merge = sum(abs(data - mean(data))) / sum(data)
    // almost identical to r_int, but without abs() in the denominator
    FloatType r_merge_den, r_meas_num, r_pim_num;

    FloatType
    merge(
      miller::index<> const& /*current_index*/,
      const FloatType* data_group, std::size_t n)
    {
      FloatType result = data_group[0];
      for(std::size_t i=1;i<n;i++) result += data_group[i];
      result /= static_cast<FloatType>(n);
      merge_equivalents::compute_r_factors(*this, data_group, n, result);
      return result;
    }

    FloatType r_int() {
      return r_int_den == 0 ? 0 : r_int_num / r_int_den;
    }

    FloatType r_merge() {
      return r_merge_den == 0 ? 0 : r_int_num / r_merge_den;
    }

    FloatType r_meas() {
      return r_merge_den == 0 ? 0 : r_meas_num / r_merge_den;
    }

    FloatType r_pim() {
      return r_merge_den == 0 ? 0 : r_pim_num / r_merge_den;
    }
  };

  template <typename FloatType=double>
  class merge_equivalents_obs
  {
    public:
      merge_equivalents_obs() :
        r_int_num(0), r_int_den(0), r_merge_den(0), r_meas_num(0), r_pim_num(0)
      {}

      merge_equivalents_obs(
        af::const_ref<index<> > const& unmerged_indices,
        af::const_ref<FloatType> const& unmerged_data,
        af::const_ref<FloatType> const& unmerged_sigmas,
        FloatType sigma_dynamic_range_=1e-6,
        bool use_internal_variance=true)
      :
        sigma_dynamic_range(sigma_dynamic_range_),
        r_int_num(0),
        r_int_den(0),
        r_merge_den(0),
        r_meas_num(0),
        r_pim_num(0)
      {
        CCTBX_ASSERT(unmerged_data.size() == unmerged_indices.size());
        CCTBX_ASSERT(unmerged_sigmas.size() == unmerged_indices.size());
        init(unmerged_indices, unmerged_data, unmerged_sigmas,
          use_internal_variance);
      }

      af::shared<index<> > indices;
      af::shared<FloatType> data;
      af::shared<FloatType> sigmas;
      FloatType sigma_dynamic_range;
      af::shared<int> redundancies;
      //! r_linear = sum(abs(data - mean(data))) / sum(abs(data))
      af::shared<FloatType> r_linear;
      //! r_square = sum((data - mean(data))**2) / sum(data**2)
      af::shared<FloatType> r_square;
      /** r_int = sum(abs(data - mean(data))) / sum(abs(data))
        where the sums run over all unique reflections but mean(data) is the
        same as for r_linear, i.e. the mean for the group of symmetry
        equivalent reflections.
      */
      FloatType r_int_num, r_int_den;
      FloatType r_merge_den, r_meas_num, r_pim_num;

      FloatType r_int() {
        return r_int_den == 0 ? 0 : r_int_num / r_int_den;
      }

      FloatType r_merge() {
        return r_merge_den == 0 ? 0 : r_int_num / r_merge_den;
      }

      FloatType r_meas() {
        return r_merge_den == 0 ? 0 : r_meas_num / r_merge_den;
      }

      FloatType r_pim() {
        return r_merge_den == 0 ? 0 : r_pim_num / r_merge_den;
      }

    protected:
      void
      init(
        af::const_ref<index<> > const& unmerged_indices,
        af::const_ref<FloatType> const& unmerged_data,
        af::const_ref<FloatType> const& unmerged_sigmas,
        bool use_internal_variance=true)
      {
        if (unmerged_indices.size() == 0) return;
        std::vector<FloatType> values;
        std::vector<FloatType> weights;
        std::size_t group_begin = 0;
        std::size_t group_end = 1;
        for(;group_end<unmerged_indices.size();group_end++) {
          if (unmerged_indices[group_end] != unmerged_indices[group_begin]) {
            process_group(group_begin, group_end,
                          unmerged_indices[group_begin],
                          unmerged_data, unmerged_sigmas,
                          values, weights, use_internal_variance);
            group_begin = group_end;
          }
        }
        process_group(group_begin, group_end,
                      unmerged_indices[group_begin],
                      unmerged_data, unmerged_sigmas,
                      values, weights, use_internal_variance);
      }

      void
      process_group(
        std::size_t group_begin,
        std::size_t group_end,
        index<> const& current_index,
        af::const_ref<FloatType> const& unmerged_data,
        af::const_ref<FloatType> const& unmerged_sigmas,
        std::vector<FloatType>& values,
        std::vector<FloatType>& weights,
        bool use_internal_variance=true)
      {
        std::size_t n = group_end - group_begin;
        if (n == 0) return;
        indices.push_back(current_index);
        values.clear();
        values.reserve(n);
        weights.clear();
        weights.reserve(n);
        FloatType sigma_threshold = 0;
        if (sigma_dynamic_range > 0) {
          FloatType max_sigma = 0;
          for(std::size_t i=0;i<n;i++) {
            FloatType s = unmerged_sigmas[group_begin+i];
            if (max_sigma < s) max_sigma = s;
          }
          sigma_threshold = max_sigma * sigma_dynamic_range;
        }
        FloatType unmerged_sigma = 0;
        for(std::size_t i=0;i<n;i++) {
          FloatType s = unmerged_sigmas[group_begin+i];
          if (s > sigma_threshold) {
            values.push_back(unmerged_data[group_begin+i]);
            weights.push_back(1 / scitbx::fn::pow2(s));
            unmerged_sigma = unmerged_sigmas[group_begin+i];
          }
        }
        if (values.size() == 0) {
          data.push_back(0);
          sigmas.push_back(0);
        }
        else if (values.size() == 1) {
          data.push_back(values[0]);
          sigmas.push_back(unmerged_sigma);
        }
        else {
          af::const_ref<FloatType> data_group(
            &*values.begin(), values.size());
          af::const_ref<FloatType> weights_group(
            &*weights.begin(), weights.size());
          scitbx::math::mean_and_variance<FloatType> mv(
            data_group, weights_group);
          data.push_back(mv.mean());
          FloatType merged_sigma;
          if (use_internal_variance) {
            merged_sigma = std::sqrt(
              std::max(
                mv.gsl_stats_wvariance()/values.size(),
                1/mv.sum_weights()));
          } else {
            merged_sigma = std::sqrt(1/mv.sum_weights());
          }
          sigmas.push_back(merged_sigma);
        }
        redundancies.push_back(n);
        merge_equivalents::compute_r_factors(
          *this, &unmerged_data[group_begin], n, data.back());
      }
  };

  /** refs: shelxl code; and
  http://www.crystal.chem.uu.nl/distr/mergehklf5/mergehklf5.html
  main difference to standard merging are the weights and replacing the
  experimental sigmas with sum(data-mean(data))/(n*(n-1)^0.5),
  if experimental sigmas are smaller
  */
  template <typename FloatType=double>
  class merge_equivalents_shelx {
    public:
      merge_equivalents_shelx() : inconsistent_eq(0) {}

      merge_equivalents_shelx(
        af::const_ref<index<> > const& unmerged_indices,
        af::const_ref<FloatType> const& unmerged_data,
        af::const_ref<FloatType> const& unmerged_sigmas)
      : r_int_num(0), r_int_den(0), r_merge_den(0), r_meas_num(0), r_pim_num(0)
      {
        CCTBX_ASSERT(unmerged_data.size() == unmerged_indices.size());
        CCTBX_ASSERT(unmerged_sigmas.size() == unmerged_indices.size());
        init(unmerged_indices, unmerged_data, unmerged_sigmas);
      }

      af::shared<index<> > indices;
      af::shared<FloatType> data;
      af::shared<FloatType> sigmas;
      af::shared<int> redundancies;
      //! r_linear = sum(abs(data - mean(data))) / sum(abs(data))
      af::shared<FloatType> r_linear;
      //! r_square = sum((data - mean(data))**2) / sum(data**2)
      af::shared<FloatType> r_square;
      /** r_int = sum(sum(abs(data - mean(data)))) / sum(sum(abs(data)))
      where inner sums run over the equivalent reflections and the
      outer ones run over all unique reflections. the r_ factors should
      be calculated in the same way as in the merge_equivalents_obs
      */
      FloatType r_int_num, r_int_den;
      FloatType r_merge_den, r_meas_num, r_pim_num;
      /** number of inconsistent equivalents:
      sum(data-mean(data))/(n*(n-1)^0.5) > 5/sum(1/sig^2),
      where n is the number of reflections in the group and mean value is
      calculated with these weights:
      weight = ((data > 3.0*sig) ? data/sig^2 : 3./sig)
      */
      std::size_t inconsistent_eq;

      FloatType r_int() { return (r_int_den == 0 ? 0 : r_int_num / r_int_den); }

      FloatType r_merge() {
        return (r_merge_den == 0 ? 0 : r_int_num / r_merge_den);
      }

      FloatType r_meas() {
        return (r_merge_den == 0 ? 0 : r_meas_num / r_merge_den);
      }

      FloatType r_pim() {
        return (r_merge_den == 0 ? 0 : r_pim_num / r_merge_den);
      }

      std::size_t inconsistent_equivalents() const { return inconsistent_eq; }
    protected:
      void
      init(
        af::const_ref<index<> > const& unmerged_indices,
        af::const_ref<FloatType> const& unmerged_data,
        af::const_ref<FloatType> const& unmerged_sigmas)
      {
        inconsistent_eq = 0;
        if (unmerged_indices.size() == 0) return;
        std::size_t group_begin = 0;
        std::size_t group_end = 1;
        for(;group_end<unmerged_indices.size();group_end++) {
          if (unmerged_indices[group_end] != unmerged_indices[group_begin]) {
            process_group(group_begin, group_end,
                          unmerged_indices[group_begin],
                          unmerged_data, unmerged_sigmas);
            group_begin = group_end;
          }
        }
        process_group(group_begin, group_end,
                      unmerged_indices[group_begin],
                      unmerged_data, unmerged_sigmas);
      }

      void
      process_group(std::size_t group_begin,
                    std::size_t group_end,
                    index<> const& current_index,
                    af::const_ref<FloatType> const& unmerged_data,
                    af::const_ref<FloatType> const& unmerged_sigmas)
      {
        std::size_t n = group_end - group_begin;
        if (n == 0) return;
        FloatType oss_sum = 0, w_sum = 0, i_wght_sum = 0;
        for(std::size_t i=0;i<n;i++) {
          const std::size_t index = group_begin+i;
          const FloatType s = (unmerged_sigmas[index] == 0 ?
            static_cast<FloatType>(1e-3) : unmerged_sigmas[index]);
          const FloatType oss = scitbx::fn::pow2(1./s);
          const FloatType val = unmerged_data[index];
          const FloatType w = ((val > 3.0*s) ? val*oss : 3.0/s);
          oss_sum += oss;
          w_sum += w;
          i_wght_sum += w*val;
        }
        const FloatType mean = i_wght_sum/w_sum;
        FloatType sum_diff = 0, sum_i = 0, sum_diffs = 0, sum_is = 0;
        for(std::size_t i=0;i<n;i++) {
          const FloatType val = unmerged_data[group_begin+i];
          const double diff = val-mean;
          sum_diff += scitbx::fn::absolute(diff);
          sum_i += val;
          sum_diffs += scitbx::fn::pow2(diff);
          sum_is += scitbx::fn::pow2(val);
        }
        CCTBX_ASSERT(oss_sum != 0);
        FloatType sig = std::sqrt(1./oss_sum);
        if (n>1) {
          r_int_num += sum_diff;
          r_int_den += sum_i;
          r_meas_num += std::sqrt((FloatType)n/(FloatType)(n-1)) * sum_diff;
          r_pim_num += std::sqrt(1.0 / (FloatType)(n-1)) * sum_diff;
          const FloatType
            sig_int = sum_diff/(n*sqrt(static_cast<double>(n)-1.0));
          if (sig_int > sig) {
            if (sig_int > 5*sig)
              inconsistent_eq++;
            sig = sig_int;  //replace the experimental sigma
          }
        }
        r_linear.push_back(sum_i == 0 ? 0 : sum_diff/sum_i);
        r_square.push_back(sum_is == 0 ? 0 : sum_diffs/sum_is);
        indices.push_back(current_index);
        data.push_back(i_wght_sum/w_sum);
        sigmas.push_back(sig);
        redundancies.push_back(n);
      }
  };

  template <typename FloatType=double>
  class split_unmerged {
    public :
      af::shared<FloatType> data_1;
      af::shared<FloatType> data_2;
      af::shared< index<> > indices;

      split_unmerged (
        af::const_ref<index<> > const& unmerged_indices,
        af::const_ref<FloatType> const& unmerged_data,
        af::const_ref<FloatType> const& unmerged_sigmas,
        bool weighted=true,
        unsigned seed=0)
      {
        if (unmerged_indices.size() == 0) return;
        if (seed != 0) gen.seed(seed);
        CCTBX_ASSERT(unmerged_sigmas.all_gt(0.0));
        std::size_t group_begin = 0;
        std::size_t group_end = 1;
        for(;group_end<unmerged_indices.size();group_end++) {
          if (unmerged_indices[group_end] != unmerged_indices[group_begin]) {
            process_group(group_begin, group_end,
                          unmerged_indices[group_begin],
                          unmerged_data, unmerged_sigmas, weighted);
            group_begin = group_end;
          }
        }
        process_group(group_begin, group_end,
                      unmerged_indices[group_begin],
                      unmerged_data, unmerged_sigmas, weighted);
      }

// XXX why doesn't this work?
//      FloatType cc_one_half () {
//        return scitbx::math::linear_regression<FloatType>(data_1,
//          data_2).coefficient();
//      }

    protected:

      void process_group (
        std::size_t group_begin,
        std::size_t group_end,
        index<> const& current_index,
        af::const_ref<FloatType> const& unmerged_data,
        af::const_ref<FloatType> const& unmerged_sigmas,
        bool weighted)
      {
        const std::size_t n = group_end - group_begin;
        if (n < 2) {
          return;
        } else {
          // temp is a copy of the array of intensites of each observation
          std::vector<FloatType> temp(n), temp_w(n);
          for(std::size_t i=0;i<n;i++) {
            temp[i] = unmerged_data[group_begin+i];
            if (weighted) {
              temp_w[i] = 1.0/(unmerged_sigmas[group_begin+i] *
                               unmerged_sigmas[group_begin+i]);
            } else {
              temp_w[i] = 1.0;
            }
          }
          std::size_t nsum = n/2;
          // actually I (Kay) don't think it matters, and we
          // don't do it in picknofm, but it's like that in the Science paper:
          if (2*nsum != n && gen.random_double() < 0.5)
            nsum += 1;
          std::vector<FloatType> i_obs(2, 0.), sum_w(2, 0.);
          for(std::size_t i=0;i<nsum;i++) {
            // choose a random index ind from 0 to n-i-1
            const std::size_t ind = i + std::min(n-i-1,
              std::size_t(gen.random_double()*(n-i)));
            i_obs[0] += temp[ind] * temp_w[ind];
            sum_w[0] += temp_w[ind];
            temp[ind] = temp[i];
            temp_w[ind] = temp_w[i];
          }
          for(std::size_t i=nsum;i<n;i++) {
            i_obs[1] += temp[i] * temp_w[i];
            sum_w[1] += temp_w[i];
          }

          data_1.push_back(i_obs[0] / sum_w[0]);
          data_2.push_back(i_obs[1] / sum_w[1]);
          indices.push_back(current_index);
        }
      }

      scitbx::random::mersenne_twister gen;
  };

}} // namespace cctbx::miller

#endif // CCTBX_MILLER_MERGE_EQUIVALENTS_H
