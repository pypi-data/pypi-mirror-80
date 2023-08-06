import microspec as usp
import microspeclib.datatypes.types as dtypes

class TestValues_of_status():
    def test_OK_is_0(self):
        assert usp.OK == 0
    def test_ERROR_is_1(self):
        assert usp.ERROR == 1
    def test_TIMEOUT_is_not_in_status_dict(self):
        assert list(usp.status_dict.values()).count('TIMEOUT')==0
    def test_0_maps_to_str_OK(self):
        assert usp.status_dict.get(usp.OK) == 'OK'
    def test_1_maps_to_str_ERROR(self):
        assert usp.status_dict.get(usp.ERROR) == 'ERROR'

class TestValues_of_led_setting():
    def test_OFF_is_0(self):
        assert usp.OFF == 0
    def test_GREEN_is_1(self):
        assert usp.GREEN == 1
    def test_RED_is_2(self):
        assert usp.RED == 2
    def test_0_maps_to_str_OFF(self):
        assert usp.led_dict.get(usp.OFF) == 'OFF'
    def test_1_maps_to_str_GREEN(self):
        assert usp.led_dict.get(usp.GREEN) == 'GREEN'
    def test_2_maps_to_str_RED(self):
        assert usp.led_dict.get(usp.RED) == 'RED'

class TestValues_of_binning():
    def test_BINNING_OFF_is_0(self):
        assert usp.BINNING_OFF == 0
    def test_BINNING_ON_is_1(self):
        assert usp.BINNING_ON == 1
    def test_0_maps_to_str_BINNING_OFF(self):
        assert usp.binning_dict.get(usp.BINNING_OFF) == 'BINNING_OFF'
    def test_1_maps_to_str_BINNING_ON(self):
        assert usp.binning_dict.get(usp.BINNING_ON) == 'BINNING_ON'

class TestValues_of_gain():
    def test_GAIN1X_is_1(self):
        assert usp.GAIN1X == 1
    def test_GAIN2_5X_is_0x25(self):
        assert usp.GAIN2_5X == 0x25
    def test_GAIN4X_is_4(self):
        assert usp.GAIN4X == 4
    def test_GAIN5X_is_5(self):
        assert usp.GAIN5X == 5
    def test_1_maps_to_str_GAIN1X(self):
        assert usp.gain_dict.get(usp.GAIN1X) == 'GAIN1X'
    def test_0x25_maps_to_str_GAIN2_5X(self):
        assert usp.gain_dict.get(usp.GAIN2_5X) == 'GAIN2_5X'
    def test_4_maps_to_str_GAIN4X(self):
        assert usp.gain_dict.get(usp.GAIN4X) == 'GAIN4X'
    def test_5_maps_to_str_GAIN5X(self):
        assert usp.gain_dict.get(usp.GAIN5X) == 'GAIN5X'

class TestValues_of_row_bitmap():
    def test_ALL_ROWS_is_0x1F(self):
        assert usp.ALL_ROWS == 0x1f
    def test_0x1F_maps_to_str_ALL_ROWS(self):
        assert usp.row_dict.get(usp.ALL_ROWS) == 'ALL_ROWS'

class TestConsistent_with_microspeclib():
    def test_OK_equals_microspeclib_StatusOK(self):
        assert usp.OK == dtypes.StatusOK
    def test_ERROR_equals_microspeclib_StatusError(self):
        assert usp.ERROR == dtypes.StatusError
    def test_OFF_equals_microspeclib_LEDOff(self):
        assert usp.OFF == dtypes.LEDOff
    def test_GREEN_equals_microspeclib_LEDGreen(self):
        assert usp.GREEN == dtypes.LEDGreen
    def test_RED_equals_microspeclib_LEDRed(self):
        assert usp.RED == dtypes.LEDRed
    def test_GAIN1X_equals_microspeclib_Gain1x(self):
        assert usp.GAIN1X == dtypes.Gain1x
    def test_GAIN2_5X_equals_microspeclib_Gain2_5x(self):
        assert usp.GAIN2_5X == dtypes.Gain2_5x
    def test_GAIN4X_equals_microspeclib_Gain4x(self):
        assert usp.GAIN4X == dtypes.Gain4x
    def test_GAIN5X_equals_microspeclib_Gain5x(self):
        assert usp.GAIN5X == dtypes.Gain5x
    def test_GAIN1X_equals_microspeclib_GainDefault(self):
        assert usp.GAIN1X == dtypes.GainDefault
    def test_ALL_ROWS_equals_microspeclib_RowsDefault(self):
        assert usp.ALL_ROWS == dtypes.RowsDefault

def test_MIN_CYCLES_is_1():
    assert usp.MIN_CYCLES == 1
def test_MAX_CYCLES_is_65500():
    assert usp.MAX_CYCLES == 65500
