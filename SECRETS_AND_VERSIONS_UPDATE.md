# Redpanda Migrator Skill - Secrets Management & Schema Versions Update

## ✅ Updates Complete!

The Redpanda Migrator skill has been enhanced with **secrets management for Cloud deployments** and **updated schema version defaults**.

---

## 🆕 **Major Changes**

### **1. Deployment Type Question (New Phase 0)**

**New Critical Question Added:**
> "What is the Redpanda Connect deployment type?"

**Options:**
- Redpanda Cloud
- Redpanda Serverless  
- Local
- Custom

**Impact:**
- **Cloud/Serverless** → Use environment variable secrets (`${SECRET_NAME}`)
- **Local/Custom** → Use direct credentials in YAML

---

### **2. Secrets Management for Cloud Deployments**

#### **Standard Secret Names by Platform**

**Redpanda Cloud/Dedicated/Serverless:**
```yaml
${REDPANDA_BROKERS}      # Seed brokers
${REDPANDA_USER}         # Username
${REDPANDA_USER_PWD}     # Password
```

**Confluent Cloud:**
```yaml
${CC_BROKERS}            # Bootstrap brokers
${CC_USER}               # API key
${CC_USER_PWD}           # API secret
```

**Custom Kafka/AWS MSK:**
```yaml
${KAFKA_BROKERS}         # Bootstrap brokers
${KAFKA_USER}            # Username
${KAFKA_USER_PWD}        # Password
```

#### **Configuration Comparison**

**Local Deployment (Plain Text):**
```yaml
input:
  redpanda_migrator:
    seed_brokers: ["localhost:9092"]
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "admin"
        password: "admin-password"
```

**Cloud Deployment (Secrets):**
```yaml
input:
  redpanda_migrator:
    seed_brokers: ["${REDPANDA_BROKERS}"]
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "${REDPANDA_USER}"
        password: "${REDPANDA_USER_PWD}"
```

---

### **3. Schema Version Default Changed**

**Before:**
- Default: `versions: latest`

**After:**
- Default: `versions: all` (recommended for production)

**Rationale:**
- `all` ensures complete schema history and compatibility
- Better for production migrations
- `latest` still available for faster/testing scenarios

**Configuration:**
```yaml
schema_registry:
  url: "http://schema-registry:8081"
  enabled: true
  versions: all      # DEFAULT (was: latest)
  interval: 10s
```

---

## 📦 **New Example Configurations**

### **Example 1: Confluent Cloud to Redpanda Cloud (with Secrets)**

File: `example-cloud-deployment-secrets.yaml`

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
```

### **Example 2: Custom Kafka to Redpanda Cloud (with Secrets)**

File: `example-kafka-to-cloud-secrets.yaml`

```yaml
input:
  redpanda_migrator:
    seed_brokers: ["${KAFKA_BROKERS}"]
    sasl:
      - mechanism: "SCRAM-SHA-512"
        username: "${KAFKA_USER}"
        password: "${KAFKA_USER_PWD}"

output:
  redpanda_migrator:
    seed_brokers: ["${REDPANDA_BROKERS}"]
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "${REDPANDA_USER}"
        password: "${REDPANDA_USER_PWD}"
    schema_registry:
      versions: all      # Full schema history
      normalize: true
```

---

## 📚 **Documentation Updates**

### **SKILL.md Updates:**

1. ✅ Added **Deployment Type** as first question (Phase 0)
2. ✅ Added **Secrets Management** section with examples
3. ✅ Updated **schema versions** default to `all`
4. ✅ Added secrets creation instructions
5. ✅ Added link to Redpanda Cloud secrets documentation

### **config-spec.md Updates:**

1. ✅ Added comprehensive **Secrets Management** section
2. ✅ Added 4 complete examples with secrets
3. ✅ Added secret naming conventions
4. ✅ Added deployment type decision tree
5. ✅ Updated schema versions default and documentation
6. ✅ Added best practices for secrets

### **question-guide.md Updates:**

1. ✅ Added **Phase 0: Deployment Type** (ask first!)
2. ✅ Added secrets naming conventions section
3. ✅ Added decision tree for secret names
4. ✅ Added example configurations by deployment type
5. ✅ Added instructions for creating secrets

---

## 🎯 **How Claude Will Handle This**

### **Question Flow:**

**Step 1: Deployment Type (NEW!)**
```
Claude: "What is the Redpanda Connect deployment type?"
User: "Redpanda Cloud"
Claude: [Uses secrets format for all credentials]
```

**Step 2: Cluster Types**
```
Claude: "What is your source cluster type?"
User: "Confluent Cloud"
Claude: [Will use ${CC_*} secrets]
```

**Step 3: Schema Migration**
```
Claude: "Do you want to migrate schemas?"
User: "Yes"
Claude: [Will use versions: all by default]
```

### **Generated Configuration:**

For **Cloud/Serverless deployment**:
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
    schema_registry:
      url: "http://sr:8081"
      versions: all      # DEFAULT
```

For **Local deployment**:
```yaml
input:
  redpanda_migrator:
    seed_brokers: ["pkc-abc.confluent.cloud:9092"]
    sasl:
      - mechanism: "PLAIN"
        username: "actual-api-key"
        password: "actual-api-secret"

output:
  redpanda_migrator:
    seed_brokers: ["localhost:9092"]
    sasl:
      - mechanism: "SCRAM-SHA-256"
        username: "admin"
        password: "admin-password"
    schema_registry:
      url: "http://localhost:8081"
      versions: all      # DEFAULT
```

---

## 📋 **Secret Creation Instructions**

Claude will now automatically provide these instructions for Cloud/Serverless deployments:

```
Since you're deploying to Redpanda Cloud/Serverless, you'll need to 
create the following secrets in the Redpanda Cloud Console:

1. Navigate to: Your Namespace → Connectors → Secrets

2. Create these secrets:
   - REDPANDA_BROKERS: Your cluster's seed brokers
   - REDPANDA_USER: Your SASL username
   - REDPANDA_USER_PWD: Your SASL password
   [Additional secrets as needed: CC_*, KAFKA_*]

3. Documentation: 
   https://docs.redpanda.com/redpanda-cloud/develop/connect/configuration/secret-management/
```

---

## 🔧 **Decision Logic**

### **Secrets Naming Logic:**

```
If deployment type is Cloud/Serverless:
  
  If cluster is Redpanda (Cloud/Dedicated/Serverless):
    Use: ${REDPANDA_BROKERS}, ${REDPANDA_USER}, ${REDPANDA_USER_PWD}
  
  Else if cluster is Confluent Cloud:
    Use: ${CC_BROKERS}, ${CC_USER}, ${CC_USER_PWD}
  
  Else if cluster is Kafka/MSK/Custom:
    Use: ${KAFKA_BROKERS}, ${KAFKA_USER}, ${KAFKA_USER_PWD}

Else (Local/Custom deployment):
  Use direct credential values in YAML
```

### **Schema Version Logic:**

```
If migrating schemas:
  Default: versions: all
  
  If user specifically requests latest only:
    Use: versions: latest
  
  Always explain the difference:
    - all: Complete history (production default)
    - latest: Current version only (faster)
```

---

## ✅ **Complete Feature Set**

### **Deployment Types Supported:**
- ✅ Redpanda Cloud
- ✅ Redpanda Serverless
- ✅ Local (self-hosted)
- ✅ Custom (on-premises)

### **Secrets Management:**
- ✅ Automatic secret format for Cloud/Serverless
- ✅ Platform-specific secret names (REDPANDA_*, CC_*, KAFKA_*)
- ✅ Plain text for Local/Custom
- ✅ Instructions for creating secrets
- ✅ Documentation links provided

### **Schema Migration:**
- ✅ Default: `versions: all` (production-ready)
- ✅ Optional: `versions: latest` (faster)
- ✅ Subject filtering (include/exclude)
- ✅ Normalization support
- ✅ Periodic sync

---

## 📊 **Updated Package Contents**

**Total Examples:** 18 (was 16)
- ✅ 2 new Cloud deployment examples with secrets
- ✅ All existing examples retained
- ✅ Comprehensive coverage of scenarios

**Documentation:**
- ✅ SKILL.md: Enhanced with deployment type and secrets
- ✅ config-spec.md: Complete secrets section added
- ✅ question-guide.md: Phase 0 deployment type added
- ✅ All examples: Updated where applicable

---

## 🎉 **Benefits**

### **Security:**
- ✅ Credentials never in plain text for Cloud deployments
- ✅ Secrets managed centrally in Redpanda Cloud
- ✅ Better security posture

### **Production Readiness:**
- ✅ Schema version default optimized for production (`all`)
- ✅ Complete schema history preserved
- ✅ Better compatibility guarantees

### **User Experience:**
- ✅ Clear deployment type question upfront
- ✅ Automatic secret format selection
- ✅ Clear instructions for secret creation
- ✅ Documentation links provided

---

## 📦 **Final Package**

**[redpanda-migrator.skill](computer:///mnt/user-data/outputs/redpanda-migrator.skill)** (29KB - Updated!)

### **What's New:**
1. ✅ Deployment type question (Phase 0)
2. ✅ Secrets management for Cloud/Serverless
3. ✅ Schema version default changed to `all`
4. ✅ 2 new example configurations
5. ✅ Comprehensive secrets documentation
6. ✅ Secret creation instructions

---

## 🚀 **Ready to Use!**

The skill now supports **secure Cloud deployments** with proper secrets management and **production-ready schema version defaults**!

Upload **[redpanda-migrator.skill](computer:///mnt/user-data/outputs/redpanda-migrator.skill)** and start generating secure, production-ready migration configurations! 🎉

---

## 📝 **Example Usage**

### **User asks:**
> "Create a migration config from Confluent Cloud to Redpanda Cloud"

### **Claude responds:**
> "I'll help you create that configuration. First, what is the Redpanda Connect deployment type? (Redpanda Cloud, Redpanda Serverless, Local, or Custom)"

### **User:**
> "Redpanda Cloud"

### **Claude:**
> "Perfect! I'll use environment variable secrets for your credentials. [Generates config with ${CC_*} and ${REDPANDA_*} secrets] 
>
> You'll need to create these secrets in Redpanda Cloud Console:
> - CC_BROKERS, CC_USER, CC_USER_PWD (for Confluent)
> - REDPANDA_BROKERS, REDPANDA_USER, REDPANDA_USER_PWD (for Redpanda)
>
> Documentation: https://docs.redpanda.com/redpanda-cloud/develop/connect/configuration/secret-management/"

---

**The skill is production-ready with enterprise-grade secrets management!** ✅
