class StmlReader:
    def __init__(self, schema_file):
        """Get schema_file as name and save file and save file as stml_file"""
        self.schema_file = schema_file
        self.lines = self._final_lines()

    def _get_file(self):
        """Open schema_file and return as file"""
        file = open(self.schema_file, 'r')
        return file

    def _get_lines(self):
        """Get lines of file"""
        file = self._get_file()
        lines = file.readlines()
        return lines

    def _clean_line(self, line):
        """Clean new lines from file"""
        line = line.rstrip('\n')
        return line

    def _final_lines(self):
        lines = self._get_lines()
        lines = [line.rstrip('\n') for line in lines]
        return lines


class StmlParser:
    def __init__(self, schema_lines):
        self.schema_lines = schema_lines
        self.schema_dict = self.parse()

    def split_key_type(self, line, num):
        """Split key: type from line"""
        if ":" in line:
            line = line.split(":")
            return line
        else:
            raise ValueError(f"Line {num} has no ':' to separate key and type")

    def parse_line(self, line, num):
        """Clean and split line, get key and type and return as
        dict with key and type"""
        # Get key and type from line split by ':'
        line = self.split_key_type(line, num)
        # Set both values of line_key and line_type
        line_key, line_type = line
        line_type = line_type.lstrip()
        return {"key": line_key, "type": line_type}

    def parse(self):
        """Run parse_line for each line and get all lines"""
        all_lines = {}
        for num, line in enumerate(self.schema_lines):
            new_line = self.parse_line(line, num+1)
            all_lines[new_line["key"]] = new_line["type"]
        return all_lines


class DataChecker:
    def __init__(self, schema: dict, data: dict):
        """Run StmlParser on file name 'schema'"""
        self.schema = schema
        self.data = data

    def check_type(self):
        """Check type from schema for each key in the dictionary, throw errors
        if the type does not match or exist"""
        line_num = 1
        for key, value in self.data.items():
            # Get type listed in schema
            stml_value = self.schema.get(key)
            # Check type and key are listed in schema
            if stml_value is None:
                return f"{key} not in schema"
            # Check if type is listed as int and can be an int
            if stml_value == "Int":
                if not int(value) == value:
                    return f"{value} not {stml_value} on line {line_num}"
            # Check if type is listed as str and if it should be
            elif stml_value == "Str":
                if not str(value) == value:
                    return f"{value} not {stml_value} on line {line_num}"
            # Check if type is a float in schema and if it should be
            elif stml_value == "Float":
                if not float(value) == value:
                    return f"{value} not {stml_value} on line {line_num}"
            elif stml_value == "Undef":
                pass
            else:
                # Check if type exists in schema
                if stml_value == "" or stml_value == " ":
                    return f"{value} has no specified type on line {line_num}"
                else:
                    # Warn the type is incorrect
                    return f"{value} has incorrect or non existent type on line {line_num}"
            line_num += 1
        return True


def schema_check(schema, data):
    """Check type and parse accordingly"""
    if isinstance(schema, str):
        # If schema is filename
        lines = StmlReader(schema).lines
        schema_dict = StmlParser(lines).schema_dict
        dataChecker = DataChecker(schema_dict, data)
    if isinstance(schema, list):
        # If schema is a list of stml
        schema_dict = StmlParser(schema).schema_dict
        dataChecker = DataChecker(schema_dict, data)
    if isinstance(schema, dict):
        # If schema is a dict of stml
        dataChecker = DataChecker(schema, data)

    valid = dataChecker.check_type()
    return valid
