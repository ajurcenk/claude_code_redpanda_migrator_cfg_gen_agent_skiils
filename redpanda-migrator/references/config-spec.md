# Redpanda Migrator Configuration Specification

Complete reference for all Redpanda Migrator YAML configuration fields.

## Base Structure

```yaml
# HTTP endpoint configuration (optional)
http:
  enabled: false

# Logger configuration (optional)
logger:
  level: INFO  # Options: TRACE, DEBUG, INFO, WARN, ERROR
  format: json  # Options: json, logfmt

# Source cluster configuration
input:
  redpanda_migrator_bundle:
    redpanda_migrator:
      # Source cluster settings
    schema_registry:
      # Source schema registry settings (optional)
    migrate_schemas_before_data: true

# Destination cluster configuration
output:
  redpanda_migrator_bundle:
    redpanda_migrator:
      # Destination cluster settings
    schema_registry:
      # Destination schema registry settings (optional)

# Monitoring configuration
metrics:
  prometheus: {}
```

## Input Configuration (Source Cluster)

### redpanda_migrator

**Required fields:**

```yaml
seed_brokers:
  - "source-broker1:9092"
  - "source-broker2:9092"
```

**Topic configuration:**

```yaml
topics:
  - '^[^_]'  # Regex pattern to match topics
regexp_topics: true  # Set to true when using regex patterns
```

To migrate specific topics (not regex):
```yaml
topics:
  - "topic1"
  - "topic2"
  - "topic3"
regexp_topics: false
```

**Consumer configuration:**

```yaml
consumer_group: "migrator_bundle"  # Consumer group name
start_from_oldest: true  # Start from beginning of topics
```

**Replication settings:**

```yaml
replication_factor_override: false  # Keep source replication factor
# OR
replication_factor_override: 3  # Override with specific value
```

**Authentication - SASL/SCRAM:**

```yaml
sasl:
  - mechanism: SCRAM-SHA-256
    username: "your-username"
    password: "your-password"
```

Options for mechanism:
- `PLAIN`
- `SCRAM-SHA-256`
- `SCRAM-SHA-512`
- `OAUTHBEARER`
- `AWS_MSK_IAM`

**Authentication - AWS MSK IAM:**

```yaml
sasl:
  - mechanism: AWS_MSK_IAM
    aws:
      enabled: true
      region: "us-east-1"
      # Optional: explicit credentials
      credentials:
        id: "ACCESS_KEY_ID"
        secret: "SECRET_ACCESS_KEY"
      # Optional: use EC2 instance role
      use_ec2_role_provider: true
```

**TLS Configuration:**

```yaml
tls:
  enabled: true
  skip_cert_verify: false  # Set to true for self-signed certs (not recommended for production)
  enable_renegotiation: false
  # Optional: custom CA certificate
  root_cas: |
    -----BEGIN CERTIFICATE-----
    ...
    -----END CERTIFICATE-----
  # OR specify file path
  root_cas_file: "/path/to/ca-cert.pem"
  # Optional: mutual TLS (mTLS)
  client_certs:
    - cert: |
        -----BEGIN CERTIFICATE-----
        ...
        -----END CERTIFICATE-----
      key: |
        -----BEGIN PRIVATE KEY-----
        ...
        -----END PRIVATE KEY-----
```

**Advanced fields:**

```yaml
client_id: "benthos"  # Client identifier
rack_id: ""  # Rack awareness ID
batch_size: 1024  # Messages per batch
commit_period: "5s"  # How often to commit offsets
topic_lag_refresh_period: "5s"  # Lag metric refresh interval
auto_replay_nacks: true  # Retry rejected messages
metadata_max_age: 5m  # How often to refresh topic metadata (reduce for faster regex topic discovery)
```

**Important note on metadata_max_age:**
- Default: `5m` (5 minutes)
- Controls how frequently regex topic patterns (`regexp_topics: true`) are re-evaluated
- Reduce to `30s` or `1m` if you need faster discovery of newly created topics
- Lower values increase metadata refresh frequency but add more broker queries
- Example: `metadata_max_age: 30s` checks for new topics matching the pattern every 30 seconds

### schema_registry (Input)

Configure when migrating schemas from source Schema Registry:

```yaml
schema_registry:
  url: "http://source-schema-registry:8081"
  include_deleted: true  # Include soft-deleted schemas
  subject_filter: ""  # Regex to filter subjects (empty = all)
  
  # Optional: Authentication
  basic_auth:
    enabled: true
    username: "registry-user"
    password: "registry-password"
  
  # Optional: TLS
  tls:
    enabled: true
    skip_cert_verify: false
```

**Subject filtering examples:**

```yaml
# Migrate all subjects
subject_filter: ""

# Migrate only subjects starting with "orders"
subject_filter: "^orders"

# Exclude subjects containing "test"
subject_exclude_filter: ".*test.*"
```

## Output Configuration (Destination Cluster)

### redpanda_migrator

**Required fields:**

```yaml
seed_brokers:
  - "destination-broker1:9092"
  - "destination-broker2:9092"
```

**Replication settings:**

```yaml
replication_factor_override: false  # Keep source replication factor
# OR
replication_factor_override: 3  # Override with specific value
```

**ACL migration:**

```yaml
sync_topic_acls: true  # Migrate topic ACLs
# Note: ALLOW WRITE is excluded, ALLOW ALL becomes ALLOW READ
```

**Consumer group offset migration:**

```yaml
consumer_groups: true  # Enable consumer group offset translation (boolean)
# OR with interval configuration:
consumer_groups:
  interval: 1m  # Sync consumer group offsets every 1 minute
# OR with interval and exclusions:
consumer_groups:
  interval: 1m
  exclude:
    - console-consumer-.*  # Exclude console consumers
    - __.*                 # Exclude internal consumer groups
    - connect.*            # Exclude Kafka Connect groups
```

**Consumer group offset translation details:**
- When set to `true` (boolean): Uses default sync behavior
- When configured as object with `interval`: Syncs offsets at specified interval
- `exclude`: List of regex patterns to exclude consumer groups from migration
- Recommended interval: `1m` to `10m` depending on lag tolerance
- Requires identical partition counts between source and destination
- Uses timestamp-based offset mapping

**Common exclusion patterns:**
```yaml
exclude:
  - console-consumer-.*     # Console consumers
  - __.*                    # Internal consumer groups
  - kminion-end-to-end.*   # Monitoring tool groups
  - connect-cluster         # Kafka Connect cluster
  - connectors-cluster      # Connectors
  - connect.*               # All connect-related groups
  - __redpanda.*            # Redpanda internal groups
```

**Topic prefix (optional):**

```yaml
topic_prefix: "migrated_"  # Add prefix to migrated topic names
```

**Schema translation:**

```yaml
translate_schema_ids: false  # Usually false to preserve schema IDs
```

**Serverless mode (Redpanda Cloud Serverless only):**

```yaml
serverless: true  # REQUIRED for Redpanda Cloud Serverless clusters
```

**Important:** Must be set to `true` when destination is Redpanda Cloud Serverless

**Topic replication factor override:**

```yaml
topic_replication_factor: 3  # Override replication factor for newly created topics
```

Use when:
- Source and destination have different replication requirements
- Example: MSK with RF=2 migrating to Redpanda Cloud with RF=3
- Only applies to topics created by the migrator

**Authentication - Same options as input:**

```yaml
sasl:
  - mechanism: SCRAM-SHA-256
    username: "dest-username"
    password: "dest-password"

tls:
  enabled: true
  skip_cert_verify: false
```

**Timeouts:**

```yaml
timeout: "10s"  # Message send timeout
request_timeout_overhead: "0s"  # Additional timeout buffer
conn_idle_timeout: "9m"  # Connection idle timeout
```

### schema_registry (Output)

Configure when migrating schemas to destination Schema Registry:

```yaml
schema_registry:
  url: "http://destination-schema-registry:8081"
  
  # Enable or disable schema registry (default: true when configured)
  enabled: true
  
  # Authentication (if required)
  basic_auth:
    enabled: true
    username: "dest-registry-user"
    password: "dest-registry-password"
  
  # TLS (if required)
  tls:
    enabled: true
    skip_cert_verify: false
  
  # Schema version migration
  versions: latest  # Options: "latest" or "all"
  
  # Synchronization interval
  interval: 10s  # How often to sync schemas (optional, default: once at startup)
  
  # Subject filtering (include patterns)
  include:
    - "orders.*"    # Include subjects matching regex
    - "users.*"     # Can specify multiple patterns
  
  # Subject filtering (exclude patterns)
  exclude:
    - ".*test.*"    # Exclude subjects matching regex
    - ".*temp.*"    # Takes precedence over include
  
  # Schema normalization
  normalize: true   # Transform schemas to canonical format (default: false)
```

**Schema synchronization behavior:**
- **Without `interval` field**: One-time sync on startup
- **With `interval` field**: Two-phase approach
  1. Initial sync when connecting to destination cluster
  2. Periodic sync at specified interval for ongoing schema updates
- Recommended intervals: `10s` to `1m` depending on schema update frequency

**Schema version options:**
- `latest`: Migrate only the latest version of each schema (faster, less history)
  - When combined with `interval`: Continuously captures new "latest" versions
  - Use for: Active schema evolution, faster migrations
- `all`: Migrate complete version history (slower, full compatibility)
  - Use for: Complete historical record, full compatibility requirements

**Subject filtering:**
- **`include`**: List of regex patterns to include specific subjects
  - Only subjects matching these patterns will be migrated
  - Examples: `["orders.*", "users.*", "^prod_.*"]`
- **`exclude`**: List of regex patterns to exclude subjects
  - Takes precedence over `include` patterns
  - Examples: `[".*test.*", ".*temp.*", ".*dev.*"]`
- **Both**: Can use together for fine-grained control
  - Include takes priority, then exclude removes from that set

**Schema normalization:**
- **`normalize: true`**: Enable schema normalization
  - Transforms schemas to canonical format before registration
  - Compares semantic equivalence rather than syntactic differences
  - Collapses duplicate schemas with different formatting
- **Use cases:**
  - Source has inconsistent schema formatting (whitespace, field order)
  - Prevent duplicate schema registrations
  - Clean up schema registry after migration
  - Maintain semantic compatibility across versions
- **Example:** These would be treated as identical with normalization:
  ```json
  {"type": "record", "name": "User", "fields": [{"name": "id", "type": "int"}]}
  {"type":"record","name":"User","fields":[{"name":"id","type":"int"}]}
  ```

**Important notes:**
- Set `enabled: false` to disable schema migration even when URL is configured
- This is useful for data-only migrations where schema registry is present but not needed
- Default is `true` when schema_registry section is present
- Destination Schema Registry must be in READWRITE or IMPORT mode

## Metrics Configuration

```yaml
metrics:
  prometheus: {}
```

This enables Prometheus metrics endpoint at `http://localhost:4195/metrics`.

Key metrics:
- `input_redpanda_migrator_lag` - Migration lag per topic/partition

## Complete Example Templates

### Example 1: Full Migration (Data + Schemas + Consumer Offsets + ACLs)

```yaml
http:
  enabled: false

input:
  redpanda_migrator_bundle:
    redpanda_migrator:
      seed_brokers:
        - "source-kafka:9092"
      topics:
        - '^[^_]'  # Skip internal topics starting with _
      regexp_topics: true
      consumer_group: "migrator_bundle"
      start_from_oldest: true
      replication_factor_override: false
      sasl:
        - mechanism: SCRAM-SHA-256
          username: "source-user"
          password: "source-password"
      tls:
        enabled: true
        skip_cert_verify: false
    schema_registry:
      url: "http://source-schema-registry:8081"
      include_deleted: true
      subject_filter: ""
      basic_auth:
        enabled: true
        username: "sr-user"
        password: "sr-password"
    migrate_schemas_before_data: true

output:
  redpanda_migrator_bundle:
    redpanda_migrator:
      seed_brokers:
        - "destination-redpanda:9092"
      replication_factor_override: false
      sync_topic_acls: true
      consumer_groups: true
      sasl:
        - mechanism: SCRAM-SHA-256
          username: "dest-user"
          password: "dest-password"
      tls:
        enabled: true
    schema_registry:
      url: "http://dest-schema-registry:8081"
      migrate_schema_versions: "all"
      sync_interval: "1m"
      basic_auth:
        enabled: true
        username: "dest-sr-user"
        password: "dest-sr-password"

metrics:
  prometheus: {}
```

### Example 2: Data-Only Migration (No Schemas, No ACLs)

```yaml
http:
  enabled: false

input:
  redpanda_migrator_bundle:
    redpanda_migrator:
      seed_brokers:
        - "source-kafka:9092"
      topics:
        - "orders"
        - "users"
        - "products"
      regexp_topics: false
      consumer_group: "data_migrator"
      start_from_oldest: true

output:
  redpanda_migrator_bundle:
    redpanda_migrator:
      seed_brokers:
        - "destination-kafka:9092"
      consumer_groups: false
      sync_topic_acls: false

metrics:
  prometheus: {}
```

### Example 3: AWS MSK to Redpanda Cloud

```yaml
http:
  enabled: false

input:
  redpanda_migrator_bundle:
    redpanda_migrator:
      seed_brokers:
        - "b-1.msk-cluster.abc123.kafka.us-east-1.amazonaws.com:9096"
      topics:
        - '^[^_]'
      regexp_topics: true
      consumer_group: "msk_migrator"
      start_from_oldest: true
      sasl:
        - mechanism: AWS_MSK_IAM
          aws:
            enabled: true
            region: "us-east-1"
            use_ec2_role_provider: true
      tls:
        enabled: true
    schema_registry:
      url: "https://glue-schema-registry.us-east-1.amazonaws.com"
      include_deleted: true

output:
  redpanda_migrator_bundle:
    redpanda_migrator:
      seed_brokers:
        - "seed-abc123.cloud.redpanda.com:9092"
      sync_topic_acls: false  # ACLs don't translate between AWS MSK and Redpanda
      consumer_groups: true
      sasl:
        - mechanism: SCRAM-SHA-256
          username: "redpanda-user"
          password: "redpanda-password"
      tls:
        enabled: true
    schema_registry:
      url: "https://schema-registry.cloud.redpanda.com:30081"
      migrate_schema_versions: "all"
      basic_auth:
        enabled: true
        username: "sr-user"
        password: "sr-password"

metrics:
  prometheus: {}
```

### Example 4: Redpanda to Redpanda (Data-Only with Consumer Offset Translation)

```yaml
http:
  enabled: false

logger:
  level: DEBUG

input:
  redpanda_migrator:
    seed_brokers: ["localhost:9092"]
    
    # Use regex pattern for topic matching
    regexp_topics: true
    topics: ["test_migrator.*"]
    
    consumer_group: "migration_test_v1"
    
    # Reduced from default 5m to 30s for faster topic discovery
    # Regex patterns re-evaluated at this interval to find new topics
    metadata_max_age: 30s
    
    schema_registry:
      url: "http://source-registry:8081"

output:
  redpanda_migrator:
    seed_brokers: ["redpanda-0.testzone.local:31092"]
    
    # Consumer group offset translation with 1-minute sync interval
    consumer_groups:
      interval: 1m
    
    # Schema registry disabled for data-only migration
    schema_registry:
      url: "http://source-registry:8081"
      enabled: false
```

## Field Reference Summary

### Consumer Offset Translation

- `output.redpanda_migrator_bundle.redpanda_migrator.consumer_groups: true` - Enables offset migration
- Requires identical partition counts between source and destination

### ACL Migration

- `output.redpanda_migrator_bundle.redpanda_migrator.sync_topic_acls: true` - Enables ACL migration
- Automatically sanitizes ACLs (excludes WRITE, downgrades ALL to READ)

### Schema Migration

- `input.redpanda_migrator_bundle.schema_registry.url` - Source Schema Registry
- `output.redpanda_migrator_bundle.schema_registry.url` - Destination Schema Registry
- `output.redpanda_migrator_bundle.schema_registry.migrate_schema_versions` - "latest" or "all"
- Destination must be in READWRITE or IMPORT mode

### Topic Filtering

- `input.redpanda_migrator_bundle.redpanda_migrator.topics` - List of topics or regex patterns
- `input.redpanda_migrator_bundle.redpanda_migrator.regexp_topics` - true for regex, false for exact names

### Replication Factor

- `input.redpanda_migrator_bundle.redpanda_migrator.replication_factor_override` - false or integer
- `output.redpanda_migrator_bundle.redpanda_migrator.replication_factor_override` - false or integer
