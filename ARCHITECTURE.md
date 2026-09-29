API nodes are stateless. Jobs land in SQLite (swap for Redis/SQS later).
After 3 failures the job moves to the dead-letter queue. Rate limit is per API key.
Job types: echo, upper, fail.
