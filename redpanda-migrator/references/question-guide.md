# Question Guide for Migration Configuration

Use this guide to systematically gather all required information for generating a Redpanda Migrator configuration.

## Questioning Strategy

Ask questions in this order to build context progressively. Don't overwhelm users with all questions at once - ask follow-up questions based on previous answers.

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
