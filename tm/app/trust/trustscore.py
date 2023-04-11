class RayChakraborty:
    """
    This class is used to calculate the trust score of a user.

    Methods in this class follow the paper:
    Ray, I., & Chakraborty, S. (2004). A vector model of trust for developing trustwor-
    thy systems. In Computer Security-ESORICS 2004: 9th European Symposium on Research
    in Computer Security, Sophia Antipolis, France, September 13-15, 2004. Proceedings
    9 (pp. 260-275). Springer Berln Heidelberg.

    The authors defined three trust purposes and three turstee aspects. However, our
    project covers the first trust purpose "to access resources" only. Also, we use
    different trustee aspects according to our trust ontology, which are the dentity
    trust and behavior trust of a trustees (users) and the identity trust of their org-
    anizations.

    They also defined three parameters that influence trust values: experience, knowle-
    dge, and recommendation. In our project, we use the experience parameter only. The
    positiveness and negativeness of the experience are decied by the user's compliance
    to a Data Use Agreement (DUA) between data custodians and the user.
    """

    def __init__(self):
        pass

    def get_weight(self, time_interval: int):
        """
        None negative weight to the ith time interval.
        """
        return 2 / (time_interval * (time_interval + 1))

    def get_experience_value(self, current_trustscore: float, incident_value: int):
        """
        This is the simplest case of the experience parameter calculation. It assumes
        there are only two time intervals: the current time interval and the previous
        time interval.

        The estimated incident value of the previous time interval is derived from the
        current trust score by multiplying sum of the number of time intervals, which
        is 3 in this case.

        - W: weighted sum of the current trust score and the incident value
        - E: experience value
        """
        W = (
            self.get_weight(2) * (current_trustscore * 3)
            + self.get_weight(1) * incident_value
        )
        E = W / 3

        return E
