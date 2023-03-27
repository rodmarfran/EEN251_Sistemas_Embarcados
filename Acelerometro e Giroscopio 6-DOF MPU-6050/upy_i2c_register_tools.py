"""!
@file upy_i2c_register_tools.py
@brief MicroPython I2C Register Tools for handling I2C registers
@details This library provides classes for handling single and multiple bit fields, structures, and arrays of structures in 
         I2C registers. It supports read-only and read-write access for the I2C registers. The library uses the ustruct library 
         for packing and unpacking data and is compatible with MicroPython.
@author Rodrigo França
@date 2023-03-28
"""

# Import ustruct library to work with primitive data functions
import ustruct

## @brief A class for managing a single read-write bit in an I2C register.
class RWBit:

    ## @brief Constructor for the RWBit class.
    #  @param reg_addr: The address of the I2C register that contains the bit.
    #  @param bit_offset: The bit position within the register, from 0 to 7.
    def __init__(self, reg_addr: int, bit_offset: int):
    
        self._reg_addr = reg_addr
        self._bit_offset = bit_offset
        self._bit_mask = 1 << bit_offset

    ## @brief Getter method for the RWBit class. Reads the value of the bit from the I2C register.
    #  @param instance: The instance of the class that contains the I2C device and address.
    #  @param owner: The class that owns the descriptor.
    #  @return The value of the bit as a boolean.
    def __get__(self, instance, owner):
    
        # Read the register value from the I2C device
        reg_value = instance._i2c.readfrom_mem(instance._i2c_addr, self._reg_addr, 1)[0]

        # Extract the value of the bit using the private constant mask
        return (reg_value & self._bit_mask) >> self._bit_offset

    ## @brief Setter method for the RWBit class. Writes a new value to the bit in the I2C register.
    #  @param instance: The instance of the class that contains the I2C device and address.
    #  @param value: The new value of the bit as a boolean.
    def __set__(self, instance, value):

        # Read the current register value from the I2C device
        reg_value = instance._i2c.readfrom_mem(instance._i2c_addr, self._reg_addr, 1)[0]

        # Update the bit value
        if value:
            reg_value |= self._bit_mask
        else:
            reg_value &= ~self._bit_mask

        # Write the updated register value to the I2C device
        instance._i2c.writeto_mem(instance._i2c_addr, self._reg_addr, bytes([reg_value]))

## @brief A class for managing a single read-only bit in an I2C register.
class ROBit(RWBit):

    ## @brief Setter method for the ROBit class. Raises an AttributeError since the bit is read-only.
    #  @param instance: The instance of the class that contains the I2C device and address.
    #  @param value: The new value of the bit as a boolean.
    def __set__(self, instance, value):
    
        raise AttributeError("This bit is read-only")

## @brief A class for managing a single read-write bit field in an I2C register.
class RWBits:

    ## @brief Constructor for RWBits class.
    #  @param bits_width: The width of the bit field.
    #  @param reg_addr: The address of the register containing the bit field.
    #  @param bits_offset: The bit offset of the bit field within the register.
    def __init__(self, bits_width: int, reg_addr: int, bits_offset: int):
        
        self._bits_width = bits_width
        self._reg_addr = reg_addr
        self._bits_offset = bits_offset
        self._bits_mask = ((1 << bits_width) - 1) << bits_offset
        self._value_mask = (1 << bits_width) - 1

    ## @brief Getter method for the RWBits class.
    #  @param instance: The instance of the class.
    #  @param owner: The class that owns the instance.
    #  @return: The value of the bit field.
    def __get__(self, instance, owner):

        # Read the register value from the I2C device
        reg_value = instance._i2c.readfrom_mem(instance._i2c_addr, self._reg_addr, 1)[0]

        # Extract the value of the bit field using the private constant mask
        return (reg_value & self._bits_mask) >> self._bits_offset

    ## @brief Setter method for the RWBits class.
    #  @param instance: The instance of the class.
    #  @param value: The new value to be set for the bit field.
    def __set__(self, instance, value):

        # Read the current register value from the I2C device
        reg_value = instance._i2c.readfrom_mem(instance._i2c_addr, self._reg_addr, 1)[0]

        # Calculate the value to write to the bit field
        value &= self._value_mask
        value <<= self._bits_offset

        # Clear the bits corresponding to the bit field and write the new value to the register
        reg_value &= ~self._bits_mask
        reg_value |= value
        instance._i2c.writeto_mem(instance._i2c_addr, self._reg_addr, bytes([reg_value]))

## @brief A class for managing a single read-only bit field in an I2C register.
class ROBits(RWBits):

    ## @brief Setter method for the ROBits class.
    #  @param instance: The instance of the class.
    #  @param value: The new value to be set for the bit field.
    def __set__(self, instance, value):

        raise AttributeError("This bit field is read-only")

## @brief A class for managing a single read-write register access using struct packing and unpacking in an I2C device.
class UnaryStruct:

    ## @brief Constructor for UnaryStruct class.
    #  @param reg_addr: The address of the register to be accessed.
    #  @param struct_format: The struct format to be used for packing and unpacking data.
    def __init__(self, reg_addr: int, struct_format: str):

        self._reg_addr = reg_addr
        self._struct_format = struct_format

    ## @brief Getter method for the UnaryStruct class.
    #  @param instance: The instance of the class.
    #  @param owner: The class that owns the instance.
    #  @return: The unpacked data from the register.
    def __get__(self, instance, owner):

        # Read the register data from the I2C device
        reg_data = instance._i2c.readfrom_mem(instance._i2c_addr, self._reg_addr, ustruct.calcsize(self._struct_format))

        # Unpack the register data using the specified struct format
        return ustruct.unpack(self._struct_format, reg_data)[0]

    ## @brief Setter method for the UnaryStruct class.
    #  @param instance: The instance of the class.
    #  @param new_data: The new data to be written to the register.
    def __set__(self, instance, new_data):

        # Pack the new data using the specified struct format
        reg_data = ustruct.pack(self._struct_format, new_data)

        # Write the packed data to the I2C register
        instance._i2c.writeto_mem(instance._i2c_addr, self._reg_addr, reg_data)

## @brief A class for managing a single read-only register access using struct packing and unpacking in an I2C device.
class ROUnaryStruct(UnaryStruct):

    ## @brief Setter method for the ROUnaryStruct class.
    #  @param instance: The instance of the class.
    #  @param new_data: The new data to be written to the register.
    def __set__(self, instance, new_data):

        raise AttributeError("This register is read-only")

## @brief A class for managing a multiple read-write array-based registers access using struct packing and unpacking in an I2C device.
class StructArray:

    ## @brief Constructor for StructArray class.
    #  @param reg_addr: The address of the register to be accessed.
    #  @param struct_format: The struct format to be used for packing and unpacking data.
    #  @param array_size: The size of the array.
    def __init__(self, reg_addr: int, struct_format: str, array_size: int):

        self._reg_addr = reg_addr
        self._struct_format = struct_format
        self._array_size = array_size
        self._element_size = ustruct.calcsize(self._struct_format)

    ## @brief Getter method for the StructArray class.
    #  @param index: The index of the element to be accessed.
    #  @param instance: The instance of the class.
    #  @return: The unpacked data from the register.
    def __getitem__(self, index, instance):

        if 0 <= index < self._array_size:
            # Calculate the address for the requested index
            addr = self._reg_addr + index * self._element_size

            # Read the register value from the I2C device
            reg_data = instance._i2c.readfrom_mem(instance._i2c_addr, addr, self._element_size)

            # Unpack the register data using the specified struct format
            return ustruct.unpack(self._struct_format, reg_data)[0]
        else:
            raise IndexError("Index out of range")

    ## @brief Setter method for the StructArray class.
    #  @param index: The index of the element to be set.
    #  @param instance: The instance of the class.
    #  @param value: The new value to be written to the register.
    def __setitem__(self, index, instance, value):
    
        if 0 <= index < self._array_size:
            # Calculate the address for the requested index
            addr = self._reg_addr + index * self._element_size

            # Pack the new value using the specified struct format
            reg_data = ustruct.pack(self._struct_format, value)

            # Write the packed data to the I2C register
            instance._i2c.writeto_mem(instance._i2c_addr, addr, reg_data)
        else:
            raise IndexError("Index out of range")

    ## @brief Getter method for the entire StructArray class.
    #  @param instance: The instance of the class.
    #  @param owner: The class that owns the instance.
    #  @return: The unpacked data for the entire array from the register.
    def __get__(self, instance, owner):

        # Calculate the address for the entire array
        addr = self._reg_addr

        # Read the entire array from the I2C device
        reg_data = instance._i2c.readfrom_mem(instance._i2c_addr, addr, self._array_size * self._element_size)

        # Unpack the register data using the specified struct format for the entire array
        return ustruct.unpack_from(self._struct_format[0] + str(self._array_size) + self._struct_format[1:], reg_data)

    ## @brief Setter method for the entire StructArray class.
    #  @param instance: The instance of the class.
    #  @param value: The new values to be written to the entire array.
    def __set__(self, instance, value):

        if len(value) != self._array_size:
            raise ValueError("Wrong number of elements in the input array")

        # Pack the entire new value tuple using the specified struct format
        reg_data = ustruct.pack(self._struct_format[0] + str(self._array_size) + self._struct_format[1:], *value)

        # Write the packed data to the entire array in the I2C register
        instance._i2c.writeto_mem(instance._i2c_addr, self._reg_addr, reg_data)
