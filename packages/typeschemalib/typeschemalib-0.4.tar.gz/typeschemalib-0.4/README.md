# lib_type_schema
A yaml like schema that can be used to check dictionaries for correct schema

## Schema file
#### schema example
```
point: Int
my_string: Str
grade: Float
```

#### data example
```json
{"point": 45, "my_string": "Hey", "grade": 4.5}
```

## Checking data for correct schema

```py
import file_reader

# Set schema file
schema_file = "test.stml"
# Set Data dictionary that corresponds to schema file
data = {"point": 45, "my_string": "Hey", "grade": 4.5}

# Check data for correct schema_file
dataChecker = file_reader.DataChecker(schema_file, data)

# Run type check to see if data corresponds
# valid will be True if schema is correct, it will throw errors otherwise
valid = dataChecker.check_type()
```

## Todo
Make schema have regex
Make schema have functions or options to validate data
