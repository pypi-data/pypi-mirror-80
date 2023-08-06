# KODE Logger

## Usage example
```python
import kode_logger


logger = kode_logger.create_json('my-context', tags=['tag1', 'tag2'], extra={'common_variable': 'value'})
logger.warning('hello', extra={
    'my_variable': 'value'
})
```

### Example of produced log message
```json
{
  "@timestamp": "2019-10-22T11:11:42.133Z",
  "message": "hello",
  "level": "WARNING",
  "pid": 40110,
  "context": "my-context",
  "tags": ["tag1", "tag2"],
  "extra": {
    "func_name": "example",
    "line": 5,
    "path": "file.py",
    "process_name": "MainProcess",
    "thread_name": "MainThread",
    "common_variable": "value",
    "my_variable": "value"
  }
}
```
