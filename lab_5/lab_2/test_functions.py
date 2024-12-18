import pytest
from unittest.mock import mock_open, patch
from functions import (
    read_the_file,
    frequency_bitwise_test,
    same_consecutive_bits_test,
    longest_sequence_of_units_in_a_block_test,
)

# Тесты для read_the_file
def test_read_the_file_success():
    with patch("builtins.open", mock_open(read_data="0101")):
        assert read_the_file("dummy.txt") == "0101"

def test_read_the_file_error():
    with pytest.raises(Exception, match="Error here:"):
        read_the_file("nonexistent.txt")

# Тесты для frequency_bitwise_test
def test_frequency_bitwise_test():
    assert frequency_bitwise_test("101010") == pytest.approx(1.0, rel=1e-2)

def test_standart_frequency_bitwise_test():
    assert frequency_bitwise_test("101010") == pytest.approx(1.0, rel=1e-2)
    
def test_boundary_frequency_bitwise_test():
    assert frequency_bitwise_test("") == pytest.approx(1.0, rel=1e-2)  # Пустая строка
    
# Тесты для same_consecutive_bits_test
def test_same_consecutive_bits_test():
    assert same_consecutive_bits_test("101010") == pytest.approx(0.10247043485974938, rel=1e-2)

# Тесты для longest_sequence_of_units_in_a_block_test
def test_longest_sequence_of_units_in_a_block_test():
    assert longest_sequence_of_units_in_a_block_test("101010") == pytest.approx(0.00224631493666842, rel=1e-2)

# Сложный тест с моками
def test_read_the_file_with_mock():
    with patch("builtins.open", mock_open(read_data="1010")) as mock_file:
        result = read_the_file("mocked_file.txt")
        mock_file.assert_called_once_with("mocked_file.txt", "r", encoding="UTF-8")
        assert result == "1010"
