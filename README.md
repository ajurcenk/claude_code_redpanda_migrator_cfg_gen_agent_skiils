# Redpanda Migrator Skill for Claude

A comprehensive skill for generating Redpanda Migrator YAML configurations to migrate data, schemas, consumer offsets, and ACLs between Kafka-compatible clusters.

---

## 📖 **Overview**

This skill enables Claude to generate production-ready Redpanda Migrator configurations for migrating between:
- Apache Kafka clusters
- Redpanda clusters (self-hosted, BYOC, Dedicated, Serverless)
- Confluent Cloud
- AWS MSK
- Azure Event Hubs
- Any Kafka-compatible system

---

## 🚀 **Quick Start**

### **For Claude.ai (Web Interface)**

1. Download `redpanda-migrator.skill` (32KB)
2. Go to Settings → Skills in Claude.ai
3. Click "Upload Skill"
4. Select the `redpanda-migrator.skill` file
5. Start asking Claude to generate migration configurations!

**Example prompt:**
```
"Create a migration config from Confluent Cloud to Redpanda Cloud 
with schema migration and consumer offset translation"
```

### **For Claude Code (CLI)**

```bash
# Install the skill
unzip redpanda-migrator.skill -d ~/.claude-code/skills/redpanda-migrator

# Use it
claude-code "Create a Redpanda migration config from Kafka to Redpanda Cloud"

# Validate generated config
python ~/.claude-code/skills/redpanda-migrator/scripts/validate_config.py config.yaml

# Run migration
rpk connect run config.yaml
```

---

## ✨ **Features**

### **Migration Capabilities**

- ✅ **Data Migration** - Topics with regex pattern support
- ✅ **Schema Migration** - One-time or periodic sync with filtering and normalization
- ✅ **Consumer Offset Translation** - Timestamp-based offset mapping
- ✅ **ACL Migration** - Topic ACLs with safety restrictions
- ✅ **Message Ordering** - Automatically preserved (hardcoded at partition level)

### **Deployment Types**

- ✅ **Redpanda Cloud** - With secrets management
- ✅ **Redpanda Serverless** - With secrets management
- ✅ **Local** - Self-hosted with direct credentials
- ✅ **Custom** - On-premises or other cloud providers

### **Authentication Support**

- ✅ **SASL/PLAIN** - Confluent Cloud API keys
- ✅ **SASL/SCRAM-SHA-256** - Redpanda Cloud standard
- ✅ **SASL/SCRAM-SHA-512** - AWS MSK
- ✅ **AWS_MSK_IAM** - IAM roles and instance profiles
- ✅ **TLS/mTLS** - Transport encryption and mutual TLS

### **Schema Migration Features**

- ✅ **Version strategies** - `all` (default, full history) or `latest` (current version)
- ✅ **Subject filtering** - Include/exclude patterns
- ✅ **Schema normalization** - Collapse semantic duplicates
- ✅ **Periodic sync** - Continuous schema updates
- ✅ **Authentication** - Basic auth and TLS support

### **Cloud Platforms**

- ✅ Redpanda Cloud Dedicated
- ✅ Redpanda Cloud Serverless
- ✅ Confluent Cloud
- ✅ AWS MSK
- ✅ Generic Kafka clusters

---

## 📋 **Change History**

### **Version 3.0.5 (Current) - December 2024**

#### **Complete Bundle Structure Removal**
- Removed all 29 `redpanda_migrator_bundle` structural references
- Updated documentation (SKILL.md, config-spec.md)
- Rewrote examples (example-full-migration.yaml, example-data-only.yaml)
- Completely rewrote validation script (validate_config.py)
- Removed "bundle" from consumer group names
- **Total references removed:** 32

**Impact:**
- Pure Redpanda Migrator v2 structure throughout
- Working validation script with v2 paths
- Simplified configurations
- Complete consistency

#### **AWS MSK Example Consolidation**
- Removed redundant `example-aws-msk.yaml`
- Kept comprehensive `example-aws-msk-to-redpanda.yaml`
- **Total examples:** 16 (down from 17)

#### **config-spec.md Regeneration**
- Updated base YAML structure to v2
- Rewrote all 4 example templates
- Updated AWS MSK example (IAM → SCRAM-SHA-512)
- Corrected all field reference paths

### **Version 3.0 - December 2024**

#### **Added: Secrets Management for Cloud Deployments**

**New Deployment Type Question:**
- Added Phase 0 question: "What is the Redpanda Connect deployment type?"
- Options: Redpanda Cloud, Redpanda Serverless, Local, Custom
- Determines whether to use secrets or plain text credentials

**Secrets Format:**
- Cloud/Serverless deployments use `${SECRET_NAME}` format
- Local/Custom deployments use plain text credentials
- Platform-specific secret names:
  - Redpanda: `${REDPANDA_BROKERS}`, `${REDPANDA_USER}`, `${REDPANDA_USER_PWD}`
  - Confluent: `${CC_BROKERS}`, `${CC_USER}`, `${CC_USER_PWD}`
  - Kafka/MSK: `${KAFKA_BROKERS}`, `${KAFKA_USER}`, `${KAFKA_USER_PWD}`

**New Examples:**
- `example-cloud-deployment-secrets.yaml` - Confluent Cloud → Redpanda Cloud with secrets
- `example-kafka-to-cloud-secrets.yaml` - Custom Kafka → Redpanda Cloud with secrets

**Documentation:**
- Added comprehensive secrets management section to SKILL.md
- Added secrets section to config-spec.md with 4 detailed examples
- Added Phase 0 deployment type to question-guide.md
- Added secret creation instructions and documentation link

#### **Changed: Schema Version Default**

**Before:**
- Default: `versions: latest`

**After:**
- Default: `versions: all` (recommended for production)

**Rationale:**
- Ensures complete schema history preservation
- Better for production migrations
- Full compatibility guarantees
- `latest` still available for faster migrations/testing

### **Version 2.0 - November 2024**

#### **Removed: max_in_flight Configuration**

**Reason:** `max_in_flight` is hardcoded to 1 in the Redpanda Migrator source code

**Changes:**
- Removed `max_in_flight: 1` from all example configurations
- Removed max_in_flight documentation from config-spec.md
- Updated SKILL.md to clarify ordering is automatic
- Removed max_in_flight validation from validate_config.py

**Updated Message:**
- Now: "Message ordering is automatically preserved (hardcoded at partition level)"
- Before: "Set max_in_flight: 1 to preserve message ordering"

#### **Removed: mapping Configuration**

**Reason:** Advanced feature that adds unnecessary complexity to examples

**Changes:**
- Removed `mapping:` blocks from example configurations
- Removed mapping documentation from config-spec.md
- Kept prometheus metrics enabled (essential for monitoring)

**Impact:**
- Cleaner, simpler configurations
- Focus on essential settings
- Users can still add mapping manually if needed

### **Version 1.0 - November 2024**

**Initial Release:**
- 16 example configurations
- Complete SKILL.md documentation
- Comprehensive config-spec.md reference
- Validation script (validate_config.py)
- Question gathering guide
- Schema migration with filtering and normalization
- Support for all major Kafka-compatible platforms

---

## 📊 **Current Statistics**

| Metric | Value |
|--------|-------|
| **Total Examples** | 17 configurations |
| **Schema Features** | 7 (filtering, normalization, versions, etc.) |
| **Cloud Platforms** | 3 (Redpanda, Confluent, AWS) |
| **Deployment Types** | 4 (Cloud, Serverless, Local, Custom) |
| **Authentication Methods** | 5 (PLAIN, SCRAM-256, SCRAM-512, IAM, mTLS) |
| **Configuration Fields** | 35+ options |
| **Documentation Lines** | ~30,000 lines |
| **Package Size** | 32KB |

---

## 📁 **Package Contents**

```
redpanda-migrator.skill (32KB)
├── SKILL.md                                    # Main skill instructions
├── scripts/
│   └── validate_config.py                      # Configuration validator
├── references/
│   ├── config-spec.md                          # Complete field reference
│   └── question-guide.md                       # Requirements gathering guide
└── assets/                                     # 17 example configurations
    ├── example-cloud-deployment-secrets.yaml   # NEW! Confluent→Redpanda Cloud
    ├── example-kafka-to-cloud-secrets.yaml     # NEW! Kafka→Redpanda Cloud
    ├── example-redpanda-to-redpanda.yaml       # Data-only migration
    ├── example-schema-migration-once.yaml      # One-time schema sync
    ├── example-schema-migration-periodic.yaml  # Continuous schema sync
    ├── example-schema-subject-filtering.yaml   # Schema include patterns
    ├── example-schema-latest-periodic.yaml     # Latest version strategy
    ├── example-schema-normalization.yaml       # Schema normalization
    ├── example-schema-filtering.yaml           # Schema filtering
    ├── example-to-redpanda-cloud-dedicated.yaml # Local→Dedicated
    ├── example-dedicated-to-serverless-data.yaml # Dedicated→Serverless
    ├── example-dedicated-to-serverless-with-schemas.yaml # Full cloud migration
    ├── example-confluent-to-redpanda.yaml      # Confluent Cloud migration
    ├── example-aws-msk-to-redpanda.yaml        # AWS MSK migration
    ├── example-aws-msk.yaml                    # AWS MSK example
    ├── example-data-only.yaml                  # Simple data migration
    └── example-full-migration.yaml             # Complete migration
```

---

## 🎯 **Supported Migration Scenarios**

### **1. Cloud to Cloud**
- Confluent Cloud → Redpanda Cloud (with secrets)
- AWS MSK → Redpanda Cloud (with secrets)
- Redpanda Dedicated → Redpanda Serverless

### **2. On-Premises to Cloud**
- Local Kafka → Redpanda Cloud (with secrets)
- Custom Kafka → Redpanda Dedicated (with secrets)

### **3. Local Migrations**
- Kafka → Redpanda (local deployment)
- Redpanda → Redpanda (data replication)

### **4. Cross-Platform**
- Any Kafka-compatible → Any Kafka-compatible

---

## 💡 **Usage Examples**

### **Example 1: Cloud Deployment with Secrets**

**User asks:**
```
"Create a migration config from Confluent Cloud to Redpanda Cloud"
```

**Claude asks:**
```
"What is the Redpanda Connect deployment type?"
```

**User responds:**
```
"Redpanda Cloud"
```

**Claude generates:**
```yaml
input:
  redpanda_migrator:
    seed_brokers: ["${CC_BROKERS}"]
    sasl:
      - mechanism: "PLAIN"
        username: "${CC_USER}"
        password: "${CC_USER_PWD}"
    tls:
      enabled: true
      enable_renegotiation: true

output:
  redpanda_migrator:
    seed_brokers: ["${REDPANDA_BROKERS}"]
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "${REDPANDA_USER}"
        password: "${REDPANDA_USER_PWD}"
    tls:
      enabled: true
    schema_registry:
      url: "http://schema-registry:8081"
      enabled: true
      versions: all  # DEFAULT
```

**Claude also provides:**
```
"You'll need to create these secrets in Redpanda Cloud Console:
- CC_BROKERS, CC_USER, CC_USER_PWD (for Confluent)
- REDPANDA_BROKERS, REDPANDA_USER, REDPANDA_USER_PWD (for Redpanda)

Documentation: https://docs.redpanda.com/redpanda-cloud/develop/connect/configuration/secret-management/"
```

### **Example 2: Local Deployment**

**User asks:**
```
"Create a migration config from local Kafka to local Redpanda with schema migration"
```

**Claude asks:**
```
"What is the Redpanda Connect deployment type?"
```

**User responds:**
```
"Local"
```

**Claude generates:**
```yaml
input:
  redpanda_migrator:
    seed_brokers: ["localhost:9092"]
    topics: ["orders.*"]
    regexp_topics: true
    consumer_group: "migrator"

output:
  redpanda_migrator:
    seed_brokers: ["localhost:9093"]
    consumer_groups: true
    schema_registry:
      url: "http://localhost:8081"
      enabled: true
      versions: all
```

---

## 🔧 **Configuration Options**

### **Essential Fields**

| Field | Description | Example |
|-------|-------------|---------|
| `seed_brokers` | Bootstrap servers | `["broker:9092"]` or `["${REDPANDA_BROKERS}"]` |
| `topics` | Topic patterns | `["orders.*", "users.*"]` |
| `regexp_topics` | Enable regex | `true` |
| `consumer_group` | Consumer group name | `"migrator"` |

### **Authentication**

| Method | Configuration |
|--------|---------------|
| SASL/PLAIN | `mechanism: "PLAIN"` (Confluent Cloud) |
| SASL/SCRAM-SHA-256 | `mechanism: "SCRAM-SHA-256"` (Redpanda) |
| SASL/SCRAM-SHA-512 | `mechanism: "SCRAM-SHA-512"` (AWS MSK) |
| AWS IAM | `mechanism: "AWS_MSK_IAM"` |

### **Schema Migration**

| Option | Values | Default | Use Case |
|--------|--------|---------|----------|
| `versions` | `all`, `latest` | `all` | Full history vs current only |
| `interval` | `10s`, `30s`, `1m` | none | Periodic sync frequency |
| `include` | `["prod_.*"]` | none | Include patterns |
| `exclude` | `[".*test.*"]` | none | Exclude patterns |
| `normalize` | `true`, `false` | `false` | Collapse duplicates |

### **Advanced Options**

| Option | Description | Default |
|--------|-------------|---------|
| `metadata_max_age` | Topic discovery refresh | `5m` |
| `consumer_groups.interval` | Offset sync frequency | none |
| `consumer_groups.exclude` | Filter consumer groups | none |
| `serverless` | Serverless mode flag | `false` |
| `topic_replication_factor` | Override RF | source RF |

---

## 🔒 **Secrets Management**

### **When to Use Secrets**

**Use secrets when:**
- Deploying to Redpanda Cloud
- Deploying to Redpanda Serverless

**Use plain text when:**
- Local development
- Self-hosted deployments
- Custom on-premises installations

### **Secret Naming Conventions**

| Platform | Brokers | Username | Password |
|----------|---------|----------|----------|
| **Redpanda** | `${REDPANDA_BROKERS}` | `${REDPANDA_USER}` | `${REDPANDA_USER_PWD}` |
| **Confluent** | `${CC_BROKERS}` | `${CC_USER}` | `${CC_USER_PWD}` |
| **Kafka/MSK** | `${KAFKA_BROKERS}` | `${KAFKA_USER}` | `${KAFKA_USER_PWD}` |

### **Creating Secrets in Redpanda Cloud**

1. Navigate to: **Your Namespace → Connectors → Secrets**
2. Click **"Create Secret"**
3. Enter secret name (e.g., `REDPANDA_BROKERS`)
4. Enter secret value (e.g., `seed-abc.cloud.redpanda.com:9092`)
5. Repeat for all required secrets

**Documentation:** https://docs.redpanda.com/redpanda-cloud/develop/connect/configuration/secret-management/

---

## ✅ **Validation**

### **Using the Validation Script**

```bash
# Validate your configuration
python ~/.claude-code/skills/redpanda-migrator/scripts/validate_config.py config.yaml
```

**The validator checks:**
- ✅ Required fields present (seed_brokers, topics)
- ✅ Schema registry consistency
- ✅ Consumer group configuration validity
- ✅ YAML syntax correctness

---

## 📚 **Documentation Files**

### **Main Documentation**
- **SKILL.md** - Complete skill instructions for Claude
- **config-spec.md** - Comprehensive field reference
- **question-guide.md** - Systematic requirements gathering

### **Change Documentation**
- **SECRETS_AND_VERSIONS_UPDATE.md** - Latest changes (v3.0)
- **MAX_IN_FLIGHT_REMOVAL.md** - Version 2.0 changes
- **MAPPING_REMOVAL.md** - Version 2.0 changes
- **COMPLETE_SUMMARY.md** - All features overview

### **User Guides**
- **QUICK_START.md** - 5-minute getting started
- **USAGE_GUIDE.md** - Comprehensive usage guide
- **CLAUDE_CODE_GUIDE.md** - CLI usage documentation
- **VISUAL_OVERVIEW.md** - Diagrams and workflows

---

## 🎓 **Best Practices**

### **1. Always Specify Deployment Type First**
Claude will ask about deployment type to determine credential format.

### **2. Use Secrets for Cloud Deployments**
Never use plain text credentials when deploying to Redpanda Cloud or Serverless.

### **3. Default to `versions: all` for Schemas**
Ensures complete schema history for production migrations.

### **4. Enable Consumer Offset Translation Carefully**
Requires identical partition counts between source and destination.

### **5. Exclude Internal Consumer Groups**
For Serverless migrations, always exclude internal groups:
```yaml
consumer_groups:
  exclude:
    - console-consumer-.*
    - __.*
    - connect.*
```

### **6. Monitor with Prometheus**
Always include metrics configuration:
```yaml
metrics:
  prometheus: {}
```

### **7. Use Validation Script**
Always validate generated configs before deployment.

---

## 🚨 **Important Notes**

### **Message Ordering**
Message ordering is **automatically preserved** at the partition level. This is hardcoded (`max_in_flight=1`) in the Redpanda Migrator source code and requires no configuration.

### **Schema Registry Mode**
Destination Schema Registry must be in **READWRITE** or **IMPORT** mode for schema migration.

### **Consumer Offset Translation**
- Uses timestamp-based offset mapping
- Requires identical partition counts
- Not exactly-once but minimizes duplication
- Best effort delivery

### **ACL Migration Safety**
- `ALLOW WRITE` permissions are excluded
- `ALLOW ALL` is downgraded to `ALLOW READ`
- Only topic ACLs are migrated

### **Serverless Requirements**
When migrating to Serverless:
- **MUST** set `serverless: true` flag
- **MUST** exclude internal consumer groups
- Use `.mpx.prd.cloud.redpanda.com` endpoints

### **Confluent Cloud Compatibility**
When migrating from Confluent Cloud:
- Use `PLAIN` authentication mechanism
- Enable `tls.enable_renegotiation: true`
- Use API key as username, API secret as password

---

## 🐛 **Troubleshooting**

### **Configuration Issues**

**Problem:** Schema migration not working
**Solution:** 
- Verify destination Schema Registry is in READWRITE/IMPORT mode
- Check authentication credentials
- Confirm schema_registry.enabled: true

**Problem:** Consumer offsets not translating
**Solution:**
- Verify partition counts match exactly
- Check consumer_groups configuration
- Ensure topics exist in destination

**Problem:** Secrets not resolving in Cloud deployment
**Solution:**
- Verify secrets created in Redpanda Cloud Console
- Check secret names match configuration exactly
- Confirm secrets are in the correct namespace

### **Validation Errors**

**Problem:** "Required field missing"
**Solution:** Add the required field (seed_brokers, topics, etc.)

**Problem:** "Schema registry misconfiguration"
**Solution:** Ensure schema_registry sections are consistent between source and destination

---

## 🔗 **Links & Resources**

### **Redpanda Documentation**
- Secrets Management: https://docs.redpanda.com/redpanda-cloud/develop/connect/configuration/secret-management/
- Redpanda Migrator: https://docs.redpanda.com/redpanda-connect/components/inputs/redpanda_migrator
- Redpanda Connect: https://docs.redpanda.com/redpanda-connect/about

### **Skill Resources**
- Claude.ai Skills: https://claude.ai/settings/skills
- Claude Code: https://claude.ai/code

---

## 💬 **Support & Feedback**

### **Getting Help**

**For skill issues:**
- Check the documentation files in the package
- Review example configurations in `assets/` directory
- Run validation script to identify configuration errors

**For Redpanda Migrator issues:**
- Consult Redpanda documentation
- Check Prometheus metrics for migration progress
- Review logs for detailed error messages

---

## 📝 **Version Information**

**Current Version:** 3.0
**Release Date:** December 2024
**Package Size:** 32KB
**Total Examples:** 17
**Compatibility:** Claude.ai and Claude Code

---

## 🎉 **Quick Reference**

### **Installation**
```bash
# Claude.ai: Upload in Settings → Skills
# Claude Code: unzip redpanda-migrator.skill -d ~/.claude-code/skills/redpanda-migrator
```

### **Generate Config**
```bash
# Web: "Create a migration config from Confluent to Redpanda Cloud"
# CLI: claude-code "Create a Redpanda migration config"
```

### **Validate**
```bash
python validate_config.py config.yaml
```

### **Run**
```bash
rpk connect run config.yaml
```

### **Monitor**
```bash
curl http://localhost:4195/metrics | grep input_redpanda_migrator_lag
```

---

## ✅ **Ready to Use!**

The Redpanda Migrator skill is production-ready with:
- ✅ Secure secrets management for Cloud deployments
- ✅ Production-optimized schema version defaults
- ✅ Comprehensive examples for all scenarios
- ✅ Complete documentation and validation tools
- ✅ Support for all major Kafka-compatible platforms

**Upload the skill and start generating production-ready migration configurations!** 🚀

---

*Last Updated: December 2024*
*Skill Version: 3.0*
