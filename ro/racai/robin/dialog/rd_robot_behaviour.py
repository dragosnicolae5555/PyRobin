import os


class RDRobotBehaviour:
    """
    <p>This is the object that ROBIN Dialogue Manager produces
    for the actuating system of the robot (Pepper in our case). This
    class only contains a {@link UIntentType} field, explaining what
    the user wants and a ``payload'' String which means different things
    as a function of {@link UIntentType}.</p>
    <p>The <b>payload</b> is always a <i>reference</i> of a concept in
    the {@link RDUniverse} in which the robot is operating and it has
    a certain meaning to <i>the client of the ROBIN Dialogue Manager</i>
    which is responsible with the creation of a meaningful {@link RDUniverse}.</p>
    <p>For instance, in our familiar PRECIS scenario, Pepper's ``controllers'' could
    create a concept reference like e.g. <i>sala 209</i> which, for them, has a coordinate
    on Pepper's internal map. For the ROBIN Dialogue Manager, these references and thus
    the payload do not mean anything.</p>
    """

    def __init__(self, user_intent_type, pay_load):
        """
        <p>Default constructor, specifying user intention and payload.</p>
        :param user_intent_type: user intention;
        :param pay_load: payload.
        """
        self.__user_intent_type = user_intent_type
        self.__pay_load = pay_load

    def get_user_intent_type(self):
        return self.__user_intent_type

    def get_pay_load(self):
        return self.__pay_load

    def __str__(self):
        return "User wants: " + self.__user_intent_type.name + os.sep \
               + "Extra info: " + self.__pay_load + os.sep
