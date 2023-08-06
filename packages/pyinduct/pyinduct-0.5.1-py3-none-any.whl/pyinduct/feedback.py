"""
This module contains all classes and functions related to the approximation of
distributed feedback as well as their implementation for simulation purposes.
"""

import numpy as np
from itertools import chain

from .registry import get_base
from .core import (get_weight_transformation, get_transformation_info,
                   calculate_scalar_product_matrix)
from .simulation import SimulationInput, parse_weak_formulation

__all__ = ["StateFeedback", "ObserverFeedback", "evaluate_transformations"]


class Feedback(SimulationInput):
    def __init__(self, feedback_law, **parse_kwargs):
        super().__init__(name=feedback_law.name)
        self.parse_kwargs = parse_kwargs
        self.ce = parse_weak_formulation(feedback_law,
                                         finalize=False,
                                         **parse_kwargs)
        self.const_term = np.sum(
            [st for st in self.ce.get_static_terms().values()])
        self.feedback_gains = dict()

    def _get_gains(self, weight_lbl, shape):
        if weight_lbl not in self.feedback_gains:
            self.feedback_gains[weight_lbl] = evaluate_transformations(
                self.ce,
                weight_lbl,
                shape,
                **self.parse_kwargs
            )
        gains = self.feedback_gains[weight_lbl]
        return gains


class StateFeedback(Feedback):
    """
    Base class for all feedback controllers that have to interact with the
    simulation environment.

    Args:
        control_law (:py:class:`.WeakFormulation`): Variational formulation of
            the control law.
    """
    def __init__(self, control_law):
        super().__init__(control_law)

    def _calc_output(self, **kwargs):
        """
        Calculates the controller output based on the current_weights.

        Keyword Args:
            weights: Current weights of the simulations state approximation.
            weights_lbl (str): Corresponding label of :code:`weights`.

        Return:
            dict: Controller output :math:`u`.
        """
        # determine feedback gain
        sim_weights = kwargs["weights"]
        gains = self._get_gains(kwargs["weight_lbl"], (1, len(sim_weights)))

        # (state) feedback u = k^T * x
        res = gains @ sim_weights

        # add constant term
        res += self.const_term

        return dict(output=res)


class ObserverFeedback(Feedback):
    """
    Wrapper class for all observer gains that have to interact with the
    simulation environment.

    Note:
        For observer gains (``observer_gain``) which are constructed
        from different test function bases, dont forget to specify
        these bases when initialization the :py:class:`.TestFunction`
        by using the keyword argument ``approx_lbl``.

    Args:
        observer_law (:py:class:`.WeakFormulation`): Variational formulation of
            the Observer gain. (Projected on a set of test functions.)
        output_error (:py:class:`.StateFeedback`): Output error
    """

    def __init__(self, observer_law, output_error):
        super().__init__(observer_law, is_observer=True)
        self.output_error = output_error

    def _calc_output(self, **kwargs):
        """
        Calculates the observer error intrusion.

        Keyword Args:
            weights: Current weights of the simulations system approximation.
            weights_lbl (str): Corresponding label of :code:`weights`.

        Return:
            dict: Observer error intrusion.
        """
        # determine observer gain
        weight_lbl = kwargs["obs_weight_lbl"]
        gains = self._get_gains(weight_lbl, (len(get_base(weight_lbl)), 1))

        # calculate output error intrusion
        res = gains * self.output_error(**kwargs)

        # add constant term
        res += self.const_term

        return dict(output=res)


def evaluate_transformations(ce, weight_label, vect_shape, is_observer=False):
    r"""
    Transform the different feedback/observer gains in ``ce`` to the basis
    ``weight_label`` and accumulate them to one gain vector.

    If the feedback gain :math:`u(t) = k^Tc(t)` was approximated with respect
    to the weights from the state
    :math:`x(z,t) = \sum_{i=1}^{n}c_i(t)\varphi_i(z)`
    the weight transformations the procedure is straight forward.
    However, in most of the time, during the simulation only the weights of some
    base :math:`\bar{x}(z,t) = \sum_{i=1}^{m} \bar{c}_i(t)\bar{\varphi}_i(z)`
    are available.
    Therefore, a weight transformation

    .. math::
        :nowrap:

        \begin{align*}
          c(t) = N^{-1}M\bar{c}(t), \qquad
          N_{(i,j)} = \langle \varphi_i(z), \varphi_j(z) \rangle, \qquad
          M_{(i,j)} = \langle \varphi_i(z), \bar{\varphi}_j(z) \rangle
        \end{align*}

    to this basis will be computed.

    The transformation of a approximated observer gain is a little bit more
    involved. Since, if one wants to know the transformation from the gain vector
    :math:`l_i = \langle l(z), \psi_i(z) \rangle, i=1,...,n`
    to the approximation with respect to another test base
    :math:`\bar{l}_j = \langle l(z), \bar{\psi}_j(z) \rangle, j=1,...,m`
    one has an additional degree of freedom with the ansatz
    :math:`l(z) = \sum_{i=1}^{k} c_i \varphi_i(z)`.

    In the most cases there is a natural choice for
    :math:`\varphi_i(z), \,\, i=1,...,k` and :math:`k`, such that the
    the transformation to the desired projections :math:`\bar{l}`
    can be acquired with little computational effort.
    However, for now these more elegant techniques are not covered in this
    method.

    Here only one method is implemented:

    .. math::
        :nowrap:

        \begin{align*}
          \langle l(z), \psi_j(z)\rangle =
          \langle \sum_{i=1}^{n} c_i \varphi_i(z), \psi_j(z)\rangle
          \quad \Rightarrow c = N^{-1} l,
          \quad N_{(i,j)} = \langle \varphi_i(z), \psi_j(z) \rangle\\
          \langle l(z), \bar{\psi}_j(z)\rangle =
          \langle \sum_{i=1}^{m} \bar{c}_i \bar{\psi}_i(z), \bar{\psi}_j(z)
          \quad \Rightarrow \bar{l} = M \bar{c},
          \quad M_{(i,j)} =
          \langle \bar{\psi}_i(z), \bar{\psi}_j(z) \rangle\\
        \end{align*}

    Finally the transformation between the weights
    :math:`c` and :math:`\bar{c}` will be computed with
    :py:class:`.get_weight_transformation`.

    For more advanced approximation and transformation
    features, take a look at upcoming tools in the symbolic simulation
    branch of pyinduct (comment from 2019/06/27).

    Warning:
        Since neither :py:class:`.CanonicalEquation` nor
        :py:class:`.StateSpace` know the target test base
        :math:`\bar{\psi}_j, j=1,...m`, which was used in the
        :py:class:`.WeakFormulation`, at the moment, the observer gain
        transformation works only if the state approximation base
        and the test base coincides. Which holds for example, for standard
        fem approximations methods and modal approximations of self
        adjoint operators.

    Args:
        ce (:py:class:`.CanonicalEquation`): Feedback/observer gain.
        weight_label (string): Label of functions the weights correspond to.
        vect_shape (tuple): Shape of the feedback vector.
        is_observer (bool): The argument `ce` is interpreted as
            feedback/observer if `observer` is False/True. Default: False

    Return:
        :class:`numpy.array`: Accumulated feedback/observer gain.
    """
    gain = np.zeros(vect_shape)
    identity = np.eye(max(vect_shape))

    for gain_label, law in ce.get_dynamic_terms().items():
        if "E" in law:
            # build eval vector
            vectors = _build_eval_vector(law)
            if any([p != 1 for p in vectors]):
                raise NotImplementedError

            # collect information
            gain_base = get_base(gain_label)
            weight_base = get_base(weight_label)
            gain_order = int(next(iter(vectors.values())).size
                             / gain_base.fractions.size) - 1
            weight_order = int(max(vect_shape) / weight_base.fractions.size) - 1

            if is_observer:
                info = get_transformation_info(
                    gain_label,
                    weight_label,
                    gain_order,
                    weight_order)
            else:
                info = get_transformation_info(
                    weight_label,
                    gain_label,
                    weight_order,
                    gain_order)

            # fetch handle
            transformation = get_weight_transformation(info)

            # evaluate
            if is_observer:
                # map the available projections to the origin weights
                org_weights_trafo = calculate_scalar_product_matrix(
                    gain_base, gain_base)
                # map the desired projections to the target weights
                tar_weights_trafo = calculate_scalar_product_matrix(
                    weight_base, weight_base)
                # map the available projections to the target projections
                gain += tar_weights_trafo @ transformation(
                    np.linalg.inv(org_weights_trafo) @ vectors[1])
            else:
                for i, iv in enumerate(identity):
                    gain[0, i] += np.dot(vectors[1], transformation(iv))

    return gain


def _build_eval_vector(terms):
    """
    Build a set of vectors that will compute the output by multiplication with
    the corresponding power of the weight vector.

    Args:
        terms (dict): coefficient vectors
    Return:
        dict: evaluation vector
    """
    orders = set(terms["E"].keys())
    powers = set(chain.from_iterable(
        [list(mat) for mat in terms["E"].values()]
    ))
    dim = next(iter(terms["E"][max(orders)].values())).shape

    vectors = {}
    for power in powers:
        vector = np.hstack([terms["E"].get(order, {}).get(power, np.zeros(dim))[:dim[0], :dim[1]]
                            for order in range(max(orders) + 1)])
        vectors.update({power: vector})

    return vectors

