# Question Guide for Migration Configuration

Use this guide to systematically gather all required information for generating a Redpanda Migrator configuration.

## Questioning Strategy

Ask questions in this order to build context progressively. Don't overwhelm users with all questions at once - ask follow-up questions based on previous answers.

## Phase 0: Deployment Type (Ask First)

### Critical Initial Question

**What is the Redpanda Connect deployment type?**
- Redpanda Cloud
- Redpanda Serverless
- Local (self-hosted)
- Custom (on-premises or other cloud)

**Why this matters:**
- **Redpanda Cloud/Serverless**: Must use environment variable secrets (${SECRET_NAME} format) for all credentials
- **Local/Custom**: Can use direct credentials in YAML configuration

**Impact on configuration:**
- If Cloud/Serverless: All seed_brokers, usernames, and passwords will use ${SECRET_NAME} format
- If Local/Custom: Direct values will be used in configuration

**Follow-up for Cloud/Serverless:**
- Inform user they need to create secrets in Redpanda Cloud Console
- Provide link: https://docs.redpanda.com/redpanda-cloud/develop/connect/configuration/secret-management/

## Phase 1: Source and Destination Basics

### Initial Questions

1. **What is your source cluster type?**
   - Apache Kafka (open source)
   - Redpanda (self-hosted or BYOC)
   - Confluent Cloud
   - AWS MSK (Managed Streaming for Kafka)
   - Azure Event Hubs
   - Other Kafka-compatible system

2. **What is your destination cluster type?**
   - Same options as source

3. **What are the bootstrap servers for your source cluster?**
   - Format: `hostname:port` or `hostname1:port1,hostname2:port2`
   - Example: `kafka-1.example.com:9092,kafka-2.example.com:9092`

4. **What are the bootstrap servers for your destination cluster?**
   - Same format as source

## Phase 2: Authentication and Security

### For Source Cluster

5. **Does your source cluster require authentication?**
   - If NO: Skip to Phase 3
   - If YES: Continue with questions 6-8

6. **What authentication method does the source cluster use?**
   - SASL/PLAIN
   - SASL/SCRAM-SHA-256
   - SASL/SCRAM-SHA-512
   - AWS IAM (for AWS MSK)
   - Other

7. **Is TLS/SSL enabled on the source cluster?**
   - If YES: Ask about certificates
     - "Do you need to provide a custom CA certificate?"
     - "Is mutual TLS (mTLS) required?"
   - If NO: Proceed

8. **Can you provide credentials for the source cluster?**
   - Username and password (for SASL)
   - AWS credentials or IAM role (for MSK)
   - Note: Inform user these will be in plain text in YAML (consider using environment variables)

### For Destination Cluster

Repeat questions 5-8 for the destination cluster.

## Phase 3: Migration Scope

9. **What do you want to migrate?**
   - Data (messages from topics)
   - Schemas (from Schema Registry)
   - Consumer group offsets
   - ACLs (Access Control Lists)
   - All of the above

### If Schemas Selected

10. **What is the URL of your source Schema Registry?**
    - Format: `http://hostname:port` or `https://hostname:port`
    - Example: `http://schema-registry:8081`

11. **What is the URL of your destination Schema Registry?**
    - Same format as source

12. **Does the Schema Registry require authentication?**
    - If YES: Collect username/password

13. **Do you want to migrate all schema versions or just the latest?**
    - Latest (faster, less history)
    - All versions (complete migration, better compatibility)

## Phase 4: Topic Configuration

14. **Which topics do you want to migrate?**
    - All topics (except internal/system topics)
    - Specific topics (provide list)
    - Topics matching a pattern (provide regex)

### If Pattern or All Topics

15. **Do you want to exclude internal topics?**
    - Suggest: `^[^_]` to exclude topics starting with `_`
    - This skips `__consumer_offsets` and other internal topics

### If Specific Topics

16. **Please provide the list of topic names:**
    - Example: `orders, users, products, transactions`

## Phase 5: Schema Filtering (If Schemas Enabled)

17. **Do you want to filter schema subjects?**
    - If NO: Migrate all schemas
    - If YES: Ask for include/exclude patterns
      - "Provide include pattern (regex)" - only migrate matching subjects
      - "Provide exclude pattern (regex)" - exclude matching subjects

## Phase 6: Advanced Configuration

18. **Do you want to override the replication factor?**
    - Keep source replication factor (recommended)
    - Override with specific value (provide number: 1, 3, 5, etc.)

19. **Do you need to translate consumer group offsets?**
    - YES if you want consumers to resume from where they left off
    - NO for fresh start or if not using consumer groups
    - Note: Requires identical partition counts

20. **Do you want to migrate ACLs?**
    - YES for complete migration with access controls
    - NO if ACLs don't apply or will be configured separately
    - Note: WRITE permissions are excluded for safety

## Phase 7: Operational Details

21. **What consumer group name should the migrator use?**
    - Default: `migrator_bundle`
    - Suggestion: Use a descriptive name like `migration_<date>`

22. **Should the migration start from the oldest messages?**
    - YES (default) - Complete migration from beginning
    - NO - Start from latest (only new messages)

23. **Do you want to include soft-deleted schemas?**
    - YES (default) - Complete schema history
    - NO - Only active schemas

## Question Decision Tree

```
START
  |
  ├─> Source and Destination Cluster Types
  |   └─> Bootstrap Servers
  |
  ├─> Authentication Required?
  |   ├─> YES: Authentication Method? → TLS? → Credentials?
  |   └─> NO: Continue
  |
  ├─> What to Migrate?
  |   ├─> Data: Topic Selection → Topic Filtering?
  |   ├─> Schemas: Schema Registry URLs → Auth? → Version Migration → Subject Filtering?
  |   ├─> Consumer Offsets: Translate? (requires partition match)
  |   └─> ACLs: Migrate?
  |
  ├─> Replication Factor Override?
  |
  └─> Operational Settings
      ├─> Consumer Group Name
      ├─> Start from Oldest?
      └─> Include Deleted Schemas?
```

## Common Scenarios and Typical Answers

### Scenario 1: Complete Kafka to Redpanda Migration

Typical answers:
- Source: Apache Kafka
- Destination: Redpanda Cloud
- Migrate: All (data, schemas, offsets, ACLs)
- Topics: All except internal (pattern: `^[^_]`)
- Replication: Keep source
- Consumer offsets: Yes
- ACLs: Yes
- Start from: Oldest

### Scenario 2: AWS MSK to Confluent Cloud

Typical answers:
- Source: AWS MSK with IAM auth
- Destination: Confluent Cloud with API key
- Migrate: Data and schemas only
- Topics: All except internal
- Schemas: All versions
- Consumer offsets: Yes
- ACLs: No (different ACL models)
- Replication: Override to 3

### Scenario 3: Data-Only Migration

Typical answers:
- Source: Any Kafka
- Destination: Any Kafka-compatible
- Migrate: Data only
- Topics: Specific list
- Consumer offsets: No
- ACLs: No
- Start from: Oldest

## Handling Missing Information

If user doesn't provide certain information:

**For optional fields:**
- Use sensible defaults documented in config-spec.md
- Mention defaults in comments

**For required fields:**
- Politely ask for the specific information needed
- Explain why it's required
- Provide examples

**For ambiguous answers:**
- Clarify with follow-up questions
- Offer common options
- Provide context on implications

## Information Validation

Before generating configuration, verify:
- Bootstrap servers have valid format (hostname:port)
- URLs are complete (include http:// or https://)
- If consumer offset translation enabled, warn about partition count requirement
- If ACL migration enabled, mention WRITE permission exclusion
- If schema migration enabled, confirm Schema Registry URLs provided

## Secrets Management for Cloud Deployments

### Secret Naming Conventions

When deployment type is **Redpanda Cloud** or **Redpanda Serverless**, use these standard secret names:

#### For Redpanda Clusters (Source or Destination)

```yaml
${REDPANDA_BROKERS}      # Seed brokers
${REDPANDA_USER}         # SASL username
${REDPANDA_USER_PWD}     # SASL password
```

**Use when:**
- Source is: Redpanda Cloud, Redpanda Dedicated, Redpanda Serverless
- Destination is: Redpanda Cloud, Redpanda Dedicated, Redpanda Serverless

#### For Confluent Cloud Clusters (Source or Destination)

```yaml
${CC_BROKERS}            # Bootstrap brokers
${CC_USER}               # API key (username)
${CC_USER_PWD}           # API secret (password)
```

**Use when:**
- Source is: Confluent Cloud
- Destination is: Confluent Cloud

#### For Custom Kafka/AWS MSK Clusters (Source or Destination)

```yaml
${KAFKA_BROKERS}         # Bootstrap brokers
${KAFKA_USER}            # SASL username
${KAFKA_USER_PWD}        # SASL password
```

**Use when:**
- Source is: Apache Kafka, AWS MSK, custom Kafka
- Destination is: Apache Kafka, AWS MSK, custom Kafka

### Decision Tree for Secret Names

```
If deployment type is Cloud/Serverless:
  
  If source cluster is Redpanda:
    Use: ${REDPANDA_BROKERS}, ${REDPANDA_USER}, ${REDPANDA_USER_PWD}
  
  If source cluster is Confluent Cloud:
    Use: ${CC_BROKERS}, ${CC_USER}, ${CC_USER_PWD}
  
  If source cluster is Kafka/MSK/Custom:
    Use: ${KAFKA_BROKERS}, ${KAFKA_USER}, ${KAFKA_USER_PWD}
  
  (Same logic applies for destination cluster)

If deployment type is Local/Custom:
  Use direct values in configuration (no secrets)
```

### Example Configurations by Deployment Type

#### Cloud Deployment: Confluent to Redpanda

```yaml
input:
  redpanda_migrator:
    seed_brokers: ["${CC_BROKERS}"]
    sasl:
      - mechanism: "PLAIN"
        username: "${CC_USER}"
        password: "${CC_USER_PWD}"

output:
  redpanda_migrator:
    seed_brokers: ["${REDPANDA_BROKERS}"]
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "${REDPANDA_USER}"
        password: "${REDPANDA_USER_PWD}"
```

#### Local Deployment: Confluent to Redpanda

```yaml
input:
  redpanda_migrator:
    seed_brokers: ["pkc-abc123.confluent.cloud:9092"]
    sasl:
      - mechanism: "PLAIN"
        username: "API_KEY_HERE"
        password: "API_SECRET_HERE"

output:
  redpanda_migrator:
    seed_brokers: ["localhost:9092"]
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "admin"
        password: "admin-password"
```

### Instructions to Provide with Cloud Configurations

When generating configurations for Cloud/Serverless deployment, always include:

**After generating the configuration, tell the user:**

"Since you're deploying to Redpanda Cloud/Serverless, you'll need to create the following secrets in the Redpanda Cloud Console:

1. Navigate to: Your Namespace → Connectors → Secrets
2. Create these secrets with appropriate values:
   - `REDPANDA_BROKERS`: Your cluster's seed brokers
   - `REDPANDA_USER`: Your SASL username  
   - `REDPANDA_USER_PWD`: Your SASL password
   - [Add CC_* or KAFKA_* secrets if applicable]

Documentation: https://docs.redpanda.com/redpanda-cloud/develop/connect/configuration/secret-management/"
