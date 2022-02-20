
import sys

sys.path.append('../../')
from onesim_tests.OneSimLinkUtils import OneSimLinkUtils


from onesim_tests.TestsRun.OneSimInitTestCase import *

class TestWingFlaps(OneSimInitTestCase):
    test_id = "ASIM-1650"
    test_name = "TestWingFlaps"
    lab_version = ""
    test_environment = ""
    oslu = None
    station_name = ""
    sim_state = None


    @classmethod
    def setUpClass(cls):
        """setUp method contains all setup to be done before the test steps execution"""
        super(TestWingFlaps, cls).setUpClass()
        OneSim = OneSimInitTestCase('default_method')

        oslu = OneSimLinkUtils.OneSimLinkUtils()
        station_name, sim_state = oslu.get_Values()

        # Allow to override default_preset of CockpitToHost message.
        dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Message_Counter'
        input_value = '1'
        oslu.inject_element_value(dbsim_element_path, input_value)
        # Enable the system operation by inserting its CB
        dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Right_Forward_Switch_Panel.Battery_Switch'
        input_value = 'ON'
        oslu.inject_element_value(dbsim_element_path, input_value)
        # Enable the system operation by putting the BAT switch in On position.
        dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Battery_Circuit_Breaker_Panel.FLAP_CONT_PB'
        input_value = 'PUSHED'
        oslu.inject_element_value(dbsim_element_path, input_value)
        pass

    @classmethod
    def tearDownClass(cls):
        """tearDown method contains clean up data/actions"""
        super(TestWingFlaps, cls).tearDownClass()
        pass

    def test_step_1_flaps_indicator(self):
        self.action = """
        A. Flaps indicator - Check
        B. Set flaps - LDG
        C. Set flaps -  TO
        D. Set flaps - UP
        E. Set flaps - TO
        F. Set flaps - LDG
        G. Set flaps - UP
        """ 

        self.expected = """
        A.1 Flaps Indicator reads - UP
        B.1 Flaps indicator reads - LDG. The indicator moves to an intermediate position between TO to LDG (after 2 SEC total) before it stops at LDG (after 3 SEC total). 
        C.1 Flaps indicator reads - TO.  The indicator moves to an intermediate position between LDG to TO (after 1 SEC total) before it stops at TO (after 2 SEC total). 
        D.1 Flaps Indicator - UP. The indicator moves to intermediate position between TO to UP (after 1 SEC total) before it stops at UP  (after 2 SEC total).
        E.1 Flaps indicator reads - TO.  The indicator moves to an intermediate position between UP to TO (after 1 SEC total) before it stops at TO (after 2 SEC total). 
        F.1 Flaps indicator reads - LDG. The indicator moves to an intermediate position between TO to LDG (after 1 SEC total) before it stops at LDG (after 2 SEC total). 
        G.1 Flaps Indicator - UP. The indicator moves to intermediate position between TO to UP  (after 2 SEC total) before it stops at UP (after 3 SEC total).
        """
        
        oslu = OneSimLinkUtils.OneSimLinkUtils() # Is it correct to call evry time OneSimLinkUtils()?
        station_name, _ = oslu.get_Values()

        # A
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'UP'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        oslu.timeout(3.0)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        required_output = 'UP'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('1 - A', flaps_indicator, required_output,'1 - A - Flaps Indicator shall be at UP position')
        # -------------------------------------

        # B 
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'DOWN' # LDG
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        oslu.timeout(2.0)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        required_output = 'LDG_TO'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('1 - B', flaps_indicator, required_output,'1 - B - Flaps Indicator shall be at LDG_TO position after the first 2 seconds')
        tik = time.monotonic()
        oslu.timeout(1.0)
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('1 - B', flaps_indicator, required_output, '1 - B - Flaps Indicator shall be at LDG position after a total of 3 seconds')
        # -------------------------------------

        # C
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'CENTER' # TO
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        oslu.timeout(1.0)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        required_output = 'LDG_TO'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('1 - C', flaps_indicator, required_output, '1 - C - Flaps Indicator shall be at LDG_TO position after the first 1 seconds')
        oslu.timeout(1.0)
        required_output = 'TO'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('1 - C', flaps_indicator, required_output, '1 - C - Flaps Indicator shall be at TO position after a total of 2 seconds')
        # -------------------------------------

        # D
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'UP'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        oslu.timeout(1.0)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        required_output = 'TO_UP'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('1 - D', flaps_indicator, required_output, '1 - D - Flaps Indicator shall be at TO_UP position after the first 1 seconds')
        oslu.timeout(1.0)
        required_output = 'UP'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('1 - D', flaps_indicator, required_output, '1 - D - Flaps Indicator shall be at UP position after a total of 2 seconds')
        # -------------------------------------

        # E
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'CENTER' # TO
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        oslu.timeout(1.0)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        required_output = 'TO_UP'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('1 - E', flaps_indicator, required_output, '1 - E - Flaps Indicator shall be at TO_UP position after the first 1 seconds')
        oslu.timeout(1.0)
        required_output = 'TO'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('1 - E', flaps_indicator, required_output, '1 - E - Flaps Indicator shall be at TO position after a total of 2 seconds')
        # -------------------------------------

        # F
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'DOWN'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        oslu.timeout(1.0)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        required_output = 'LDG_TO'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('1 - F', flaps_indicator, required_output, '1 - F - Flaps Indicator shall be at LDG_TO position after the first 1 seconds')
        oslu.timeout(1.0)
        required_output = 'TO'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('1 - F', flaps_indicator, required_output, '1 - F - Flaps Indicator shall be at TO position after a total of 2 seconds')
        # -------------------------------------

        # G
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'UP'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        oslu.timeout(2.0)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        required_output = 'TO_UP'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('1 - G', flaps_indicator, required_output, '1 - G - Flaps Indicator shall be at TO_UP position after the first 2 seconds')
        oslu.timeout(1.0)
        required_output = 'UP'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('1 - G', flaps_indicator, required_output, '1 - G - Flaps Indicator shall be at UP position after a total of 3 seconds')
        # -------------------------------------

    def test_step_2_operation_and_indication(self):
        self.action = """
        A. Circuit breaker FLAP CONT - Pull (BAT BUS PANEL)
        A.1. Set flaps - TO
        A.2. Set flaps - UP
        A.3. Set flaps - LDG
        B. Circuit breaker FLAP CONT - Push inside (BAT BUS PANEL)
        """
        self.expected = """
        A. The flaps position indication is unavailable - the pointer is in a position counterclockwise of the UP position.
        A.1. Flaps operation is unavailable
        A.2. Flaps operation is unavailable
        A.3. Flaps operation is unavailable
        B. The flaps position indication is available -the pointer is in up position.
        """
        oslu = OneSimLinkUtils.OneSimLinkUtils() # Is it correct to call evry time OneSimLinkUtils()?
        station_name, _ = oslu.get_Values()

        # A
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'UP'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        # Do we need to wait here as in test step 1?
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Battery_Circuit_Breaker_Panel.FLAP_CONT_PB'
        inject_value = 'RELEASED'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        # -------------------------------------

        # A.1
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'CENTER'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        oslu.timeout(2.0)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        required_output = 'UP'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('2 - A.1', flaps_indicator, required_output, '2 - A.1 - Flaps Indicator shall be at UP position because FLAB CONT is released')
        # -------------------------------------

        # A.2
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'UP'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        oslu.timeout(2.0)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('2 - A.2', flaps_indicator, required_output, '2 - A.2 - Flaps Indicator shall be at UP position because FLAB CONT is released')
        # -------------------------------------

        # A.3
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'DOWN'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        oslu.timeout(3.0)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('2 - A.3', flaps_indicator, required_output, '2 - A.3 - Flaps Indicator shall be at UP position because FLAB CONT is released')
        # -------------------------------------

        # B
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Battery_Circuit_Breaker_Panel.FLAP_CONT_PB'
        inject_value = 'PUSHED'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        # Do we need to wait here as in test step 1?
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('2 - B', flaps_indicator, required_output, '2 - B - Flaps Indicator shall be at UP position because FLAB CONT is released')
        # -------------------------------------

    def test_step_3_emergency_flaps_operation(self):
        self.action = """
        A. Circuit breaker FLAP CONT - Pull (BAT BUS PANEL)
        B.1 Emergency gear handle - Pull (by pushing the button
        on the EMER LDG GR handle and pulling the EMER LDG
        GR handle out)
        B.2 Set flaps - TO
        B.3 Set flaps - LDG
        B.4 Set flaps - UP
        C. Circuit breaker FLAP CONT - RESET  (BAT BUS PANEL)
        D. Set flaps - TO
        E. Set flaps - LDG
        F. Set flaps - TO
        G. Set flaps - UP
        """
        self.expected = """
        B.2  Emergency flap operation is not available.
        B.3  Emergency flap operation is not available.
        B.4  Emergency flap operation is not available.
        C. Flaps indicator - UP
        D. Flaps indicator - TO
        E. Flaps indicator - LDG
        F. Flaps stays at LDG position
        G. Flaps stays at LDG position
        """
        
        oslu = OneSimLinkUtils.OneSimLinkUtils() # Is it correct to call evry time OneSimLinkUtils()?
        station_name, _ = oslu.get_Values()

        # A
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'UP'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        # Do we need to wait here as in test step 1?
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Battery_Circuit_Breaker_Panel.FLAP_CONT_PB'
        inject_value = 'RELEASED'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        # -------------------------------------

        # B.1
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Emergency_Gear_Extention_Handle'
        inject_value = 'PULLED'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        # Do we need to wait here as in test step 1?
        # -------------------------------------

        # B.2
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'CENTER'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        oslu.timeout(2.0)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        required_output = 'UP'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('3 - B.2', flaps_indicator, required_output, '3 - B.2 - Flaps Indicator shall be at UP position because FLAB CONT is released and emergency gear handle is released')
        # -------------------------------------

        # B.3
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'DOWN'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        oslu.timeout(3.0)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('3 - B.3', flaps_indicator, required_output, '3 - B.3 - Flaps Indicator shall be at UP position because FLAB CONT is released and emergency gear handle is released')
        # -------------------------------------

        # B.4
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'UP'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        oslu.timeout(3.0)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('3 - B.4', flaps_indicator, required_output, '3 - B.4 - Flaps Indicator shall be at UP position because FLAB CONT is released and emergency gear handle is released')
        # -------------------------------------

        # C
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Battery_Circuit_Breaker_Panel.FLAP_CONT_PB'
        inject_value = 'PUSHED'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)

        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('3 - C', flaps_indicator, required_output, '3 - C - Flaps Indicator shall be at UP position because FLAB CONT is pushed')
        # -------------------------------------

        # D
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'CENTER'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        oslu.timeout(2.0)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        required_output = 'TO'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('3 - D', flaps_indicator, required_output, '3 - D - Flaps Indicator shall be at TO position because FLAB CONT is pushed')
        # -------------------------------------

        # E
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'DOWN'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        oslu.timeout(2.0)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        required_output = 'LDG'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('3 - E', flaps_indicator, required_output, '3 - E - Flaps Indicator shall be at LDG position because FLAB CONT is pushed')
        # -------------------------------------

        # F
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'CENTER'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        oslu.timeout(2.0)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        required_output = 'LDG'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('3 - F', flaps_indicator, required_output, '3 - F - Flaps Indicator shall be at LDG position because FLAB CONT is pushed') 
        # -------------------------------------

        # G
        inject_dbsim_element_path = station_name + '.OwnshipPanels.CockpitToHost.Throttle.Flap_selector_lever'
        inject_value = 'UP'
        oslu.inject_element_value(inject_dbsim_element_path, inject_value)
        read_dbsim_element_path = station_name + '.OwnshipPanels.HostToCockpit.Flap_Indicator'
        required_output = 'LDG'
        flaps_indicator = oslu.getSimEngineValue(read_dbsim_element_path, 'str')
        self.checkEqual('3 - G', flaps_indicator, required_output, '3 - G - Flaps Indicator shall be at LDG position because FLAB CONT is pushed')
        # -------------------------------------


if __name__ == '__main__':
    ut.main()

