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

# Source cluster configuration
input:
  redpanda_migrator:
    # Source cluster settings (seed_brokers, topics, etc.)
    
    # Source schema registry (optional)
    schema_registry:
      url: "http://source-schema-registry:8081"

# Destination cluster configuration
output:
  redpanda_migrator:
    # Destination cluster settings (seed_brokers, consumer_groups, etc.)
    
    # Destination schema registry (optional)
    schema_registry:
      url: "http://dest-schema-registry:8081"
      enabled: true
      versions: all

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
  versions: all  # Options: "all" (DEFAULT - full history) or "latest" (current version only)
  
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
- `all`: Migrate complete version history (DEFAULT - recommended for production)
  - Ensures full schema compatibility and history preservation
  - Use for: Production migrations, complete historical record, full compatibility requirements
- `latest`: Migrate only the latest version of each schema (faster, less history)
  - When combined with `interval`: Continuously captures new "latest" versions
  - Use for: Active schema evolution, faster migrations, testing scenarios

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

## Secrets Management for Cloud Deployments

When deploying Redpanda Connect to **Redpanda Cloud** or **Redpanda Serverless**, always use environment variable secrets for credentials instead of plain text values.

### Deployment Type Decision

**Ask the user:** "What is the Redpanda Connect deployment type?"
- **Redpanda Cloud** → Use secrets (${SECRET_NAME} format)
- **Redpanda Serverless** → Use secrets (${SECRET_NAME} format)
- **Local** → Use direct credentials in YAML
- **Custom** → Use direct credentials in YAML

### Standard Secret Names by Platform

#### Redpanda Cloud/Dedicated/Serverless

```yaml
${REDPANDA_BROKERS}     # Seed brokers (comma-separated)
${REDPANDA_USER}        # Username for authentication
${REDPANDA_USER_PWD}    # Password for authentication
```

#### Confluent Cloud

```yaml
${CC_BROKERS}           # Bootstrap brokers (comma-separated)
${CC_USER}              # API key (username)
${CC_USER_PWD}          # API secret (password)
```

#### AWS MSK / Custom Kafka

```yaml
${KAFKA_BROKERS}        # Bootstrap brokers (comma-separated)
${KAFKA_USER}           # Username for authentication
${KAFKA_USER_PWD}       # Password for authentication
```

### Secrets Configuration Examples

#### Example 1: Redpanda Cloud to Redpanda Cloud

```yaml
http:
  enabled: false

input:
  redpanda_migrator:
    seed_brokers: ["${REDPANDA_BROKERS}"]
    topics: ["orders.*"]
    regexp_topics: true
    consumer_group: "migrator"
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "${REDPANDA_USER}"
        password: "${REDPANDA_USER_PWD}"
    tls:
      enabled: true

output:
  redpanda_migrator:
    seed_brokers: ["${REDPANDA_BROKERS}"]
    consumer_groups: true
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "${REDPANDA_USER}"
        password: "${REDPANDA_USER_PWD}"
    tls:
      enabled: true

metrics:
  prometheus: {}
```

#### Example 2: Confluent Cloud to Redpanda Cloud

```yaml
http:
  enabled: false

input:
  redpanda_migrator:
    seed_brokers: ["${CC_BROKERS}"]
    topics: ["hello.*"]
    regexp_topics: true
    consumer_group: "migration_test_v3"
    metadata_max_age: 30s
    tls:
      enabled: true
      enable_renegotiation: true
    sasl:
      - mechanism: "PLAIN"
        username: "${CC_USER}"
        password: "${CC_USER_PWD}"

output:
  redpanda_migrator:
    seed_brokers: ["${REDPANDA_BROKERS}"]
    consumer_groups:
      interval: 10s
    tls:
      enabled: true
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "${REDPANDA_USER}"
        password: "${REDPANDA_USER_PWD}"

metrics:
  prometheus: {}
```

#### Example 3: Custom Kafka to Redpanda Cloud

```yaml
http:
  enabled: false

input:
  redpanda_migrator:
    seed_brokers: ["${KAFKA_BROKERS}"]
    topics: ["hello.*"]
    regexp_topics: true
    consumer_group: "migration_test_v3"
    metadata_max_age: 30s
    tls:
      enabled: true
    sasl:
      - mechanism: "SCRAM-SHA-512"
        username: "${KAFKA_USER}"
        password: "${KAFKA_USER_PWD}"
    schema_registry:
      url: "http://kafka-schema-registry:8081"

output:
  redpanda_migrator:
    seed_brokers: ["${REDPANDA_BROKERS}"]
    consumer_groups:
      interval: 10s
    tls:
      enabled: true
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "${REDPANDA_USER}"
        password: "${REDPANDA_USER_PWD}"
    schema_registry:
      url: "http://redpanda-schema-registry:8081"
      enabled: true
      versions: all

metrics:
  prometheus: {}
```

#### Example 4: AWS MSK to Redpanda Serverless

```yaml
http:
  enabled: false

input:
  redpanda_migrator:
    seed_brokers: ["${KAFKA_BROKERS}"]
    topics: ["prod_.*"]
    regexp_topics: true
    consumer_group: "msk_migrator"
    tls:
      enabled: true
    sasl:
      - mechanism: "SCRAM-SHA-512"
        username: "${KAFKA_USER}"
        password: "${KAFKA_USER_PWD}"

output:
  redpanda_migrator:
    seed_brokers: ["${REDPANDA_BROKERS}"]
    consumer_groups:
      interval: 1m
      exclude:
        - console-consumer-.*
        - __.*
    tls:
      enabled: true
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "${REDPANDA_USER}"
        password: "${REDPANDA_USER_PWD}"
    serverless: true

metrics:
  prometheus: {}
```

### Creating Secrets in Redpanda Cloud

For Redpanda Cloud or Serverless deployments:

1. **Create secrets** in Redpanda Cloud Console:
   - Navigate to: Namespace → Connectors → Secrets
   - Create each required secret with appropriate names
   
2. **Set secret values:**
   - `REDPANDA_BROKERS`: Your cluster's seed brokers (e.g., "seed-abc.cloud.redpanda.com:9092")
   - `REDPANDA_USER`: Your SASL username
   - `REDPANDA_USER_PWD`: Your SASL password
   - Similar pattern for CC_* (Confluent) or KAFKA_* (custom) secrets

3. **Reference in configuration:**
   - Use `${SECRET_NAME}` format in YAML
   - Never use plain text credentials

**Documentation:** https://docs.redpanda.com/redpanda-cloud/develop/connect/configuration/secret-management/

### Local vs Cloud Configuration Comparison

#### Local/Custom Deployment (Plain Text)

```yaml
input:
  redpanda_migrator:
    seed_brokers: ["localhost:9092"]
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "admin"
        password: "admin-password"
```

#### Cloud/Serverless Deployment (Secrets)

```yaml
input:
  redpanda_migrator:
    seed_brokers: ["${REDPANDA_BROKERS}"]
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "${REDPANDA_USER}"
        password: "${REDPANDA_USER_PWD}"
```

### Best Practices

1. **Always use secrets** for Cloud/Serverless deployments
2. **Use consistent naming** based on platform (REDPANDA_*, CC_*, KAFKA_*)
3. **Document secret names** in your deployment documentation
4. **Never commit** configurations with plain text credentials to version control
5. **Rotate secrets** periodically for security

## Complete Example Templates

### Example 1: Full Migration (Data + Schemas + Consumer Offsets + ACLs)

```yaml
http:
  enabled: false

logger:
  level: INFO

input:
  redpanda_migrator:
    seed_brokers: ["source-kafka:9092"]
    
    topics: ["^[^_]"]  # Skip internal topics starting with _
    regexp_topics: true
    
    consumer_group: "migrator_full"
    
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "source-user"
        password: "source-password"
    
    tls:
      enabled: true
    
    schema_registry:
      url: "http://source-schema-registry:8081"
      basic_auth:
        enabled: true
        username: "sr-user"
        password: "sr-password"

output:
  redpanda_migrator:
    seed_brokers: ["destination-redpanda:9092"]
    
    sync_topic_acls: true
    consumer_groups: true
    
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "dest-user"
        password: "dest-password"
    
    tls:
      enabled: true
    
    schema_registry:
      url: "http://dest-schema-registry:8081"
      enabled: true
      versions: all
      interval: 1m
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
  redpanda_migrator:
    seed_brokers: ["source-kafka:9092"]
    
    topics: ["orders", "users", "products"]
    regexp_topics: false
    
    consumer_group: "data_migrator"

output:
  redpanda_migrator:
    seed_brokers: ["destination-kafka:9092"]
    
    consumer_groups: false
    sync_topic_acls: false

metrics:
  prometheus: {}
```

### Example 3: AWS MSK to Redpanda Cloud

```yaml
# AWS MSK to Redpanda Cloud Dedicated
# Authentication: SCRAM-SHA-512 for MSK, SCRAM-SHA-256 for Redpanda
# Includes: Data migration, consumer offsets, replication factor override

logger:
  level: DEBUG

input:
  redpanda_migrator:
    # AWS MSK bootstrap servers
    seed_brokers: ["b-1.msk-cluster-name.xxxxx.kafka.us-east-1.amazonaws.com:9096"]
    
    regexp_topics: true
    topics: ["msk.*"]
    
    consumer_group: "migration_test_v1"
    metadata_max_age: 30s
    
    tls:
      enabled: true
    
    # AWS MSK SCRAM authentication
    sasl:
      - mechanism: "SCRAM-SHA-512"
        username: "msk-username"
        password: "msk-password"
    
    schema_registry:
      url: "https://glue-schema-registry.us-east-1.amazonaws.com"

output:
  redpanda_migrator:
    seed_brokers: ["seed-abc123.fmc.prd.cloud.redpanda.com:9092"]
    
    consumer_groups:
      interval: 10s
    
    tls:
      enabled: true
    
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "redpanda-username"
        password: "redpanda-password"
    
    # Override replication factor (MSK RF=2 → Redpanda RF=3)
    topic_replication_factor: 3
    
    schema_registry:
      url: "https://schema-registry-abc123.fmc.prd.cloud.redpanda.com:30081"
      enabled: true
      versions: all
      basic_auth:
        enabled: true
        username: "sr-username"
        password: "sr-password"

metrics:
  prometheus: {}
```

**Note:** This example shows SCRAM authentication. For IAM authentication with AWS MSK, use:
```yaml
input:
  redpanda_migrator:
    sasl:
      - mechanism: AWS_MSK_IAM
        aws:
          enabled: true
          region: "us-east-1"
          use_ec2_role_provider: true
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

- `output.redpanda_migrator.consumer_groups: true` - Enables offset migration
- Requires identical partition counts between source and destination

### ACL Migration

- `output.redpanda_migrator.sync_topic_acls: true` - Enables ACL migration
- Automatically sanitizes ACLs (excludes WRITE, downgrades ALL to READ)

### Schema Migration

- `input.redpanda_migrator.schema_registry.url` - Source Schema Registry
- `output.redpanda_migrator.schema_registry.url` - Destination Schema Registry
- `output.redpanda_migrator.schema_registry.enabled` - Enable/disable schema migration
- `output.redpanda_migrator.schema_registry.versions` - Version strategy (`all` or `latest`)
- `output.redpanda_migrator.schema_registry.interval` - Periodic sync interval

### Replication

- `output.redpanda_migrator.topic_replication_factor` - Override replication factor for new topics

### Serverless Mode

- `output.redpanda_migrator.serverless: true` - Required for Redpanda Cloud Serverless
- `output.redpanda_migrator.schema_registry.versions` - "all" (default) or "latest"
- Destination must be in READWRITE or IMPORT mode

### Topic Filtering

- `input.redpanda_migrator.topics` - List of topics or regex patterns
- `input.redpanda_migrator.regexp_topics` - true for regex, false for exact names

### Replication Factor

- `output.redpanda_migrator.topic_replication_factor` - Override replication factor for new topics
