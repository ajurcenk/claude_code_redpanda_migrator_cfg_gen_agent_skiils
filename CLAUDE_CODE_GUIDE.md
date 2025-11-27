# Redpanda Migrator Skill - Claude Code Installation Guide

## What is Claude Code?

Claude Code is Anthropic's command-line tool for agentic coding. It lets developers delegate coding tasks to Claude directly from their terminal. Skills extend Claude Code's capabilities with specialized knowledge and workflows.

---

## 📦 Installing the Redpanda Migrator Skill

### Option 1: Using the .skill File (Recommended)

The `redpanda-migrator.skill` file is a standard ZIP archive that can be used with both Claude.ai web interface and Claude Code.

**For Claude Code:**

1. **Extract the skill to your Claude Code skills directory:**

```bash
# Default Claude Code skills directory
SKILLS_DIR="$HOME/.claude-code/skills"

# Create the directory if it doesn't exist
mkdir -p "$SKILLS_DIR"

# Extract the skill (the .skill file is a ZIP)
unzip redpanda-migrator.skill -d "$SKILLS_DIR/redpanda-migrator"
```

2. **Verify installation:**

```bash
ls "$HOME/.claude-code/skills/redpanda-migrator/"
```

You should see:
- SKILL.md
- scripts/
- references/
- assets/

3. **Use with Claude Code:**

```bash
# Navigate to your project directory
cd /path/to/your/migration/project

# Ask Claude Code to generate a configuration
claude-code "Create a Redpanda migration config from Kafka to Redpanda Cloud"
```

### Option 2: Manual Installation from Source

If you have the skill source directory:

```bash
# Copy the skill directory
cp -r /path/to/redpanda-migrator "$HOME/.claude-code/skills/"
```

---

## 🎯 Using the Skill with Claude Code

### Basic Usage

```bash
# Generate a migration configuration
claude-code "Create a migration config from Confluent Cloud to Redpanda"

# Generate with specific requirements
claude-code "Generate a Redpanda Migrator YAML for AWS MSK to Redpanda Cloud with schema migration and consumer offset translation"

# Get help with configuration
claude-code "Explain the schema normalization option in Redpanda Migrator"
```

### Advanced Usage

**Generate and validate:**
```bash
# Generate config
claude-code "Create a Dedicated to Serverless migration config" > migration.yaml

# Validate using the included script
python ~/.claude-code/skills/redpanda-migrator/scripts/validate_config.py migration.yaml
```

**Interactive configuration:**
```bash
# Start an interactive session
claude-code --chat

# Then ask questions:
> I need a migration configuration
> Source: AWS MSK with SCRAM-SHA-512
> Destination: Redpanda Cloud Dedicated
> Include schema migration with normalization
```

---

## 📚 Accessing Skill Documentation

### View skill contents:

```bash
# Read main skill documentation
cat ~/.claude-code/skills/redpanda-migrator/SKILL.md

# View configuration specification
cat ~/.claude-code/skills/redpanda-migrator/references/config-spec.md

# Browse examples
ls -la ~/.claude-code/skills/redpanda-migrator/assets/
cat ~/.claude-code/skills/redpanda-migrator/assets/example-confluent-to-redpanda.yaml
```

### Quick reference:

```bash
# Create aliases for easy access
alias rp-skill-docs='cat ~/.claude-code/skills/redpanda-migrator/SKILL.md'
alias rp-skill-examples='ls -la ~/.claude-code/skills/redpanda-migrator/assets/'
alias rp-validate='python ~/.claude-code/skills/redpanda-migrator/scripts/validate_config.py'
```

---

## 🔧 Workflow Examples

### Example 1: Quick Configuration Generation

```bash
# Generate configuration
claude-code "Create a data-only migration from local Kafka to Redpanda Cloud" > migration.yaml

# Review
cat migration.yaml

# Validate
python ~/.claude-code/skills/redpanda-migrator/scripts/validate_config.py migration.yaml

# Run migration
rpk connect run migration.yaml
```

### Example 2: Iterative Development

```bash
# Start with basic config
claude-code "Generate basic Redpanda migration config" > base.yaml

# Refine based on requirements
claude-code "Add schema migration with normalization to base.yaml" > enhanced.yaml

# Add consumer group filtering
claude-code "Add consumer group exclusions for Serverless to enhanced.yaml" > final.yaml

# Validate
python ~/.claude-code/skills/redpanda-migrator/scripts/validate_config.py final.yaml
```

### Example 3: Multi-Environment Setup

```bash
# Development environment
claude-code "Create dev migration config: local Kafka to local Redpanda" > dev-migration.yaml

# Staging environment
claude-code "Create staging migration config: AWS MSK to Redpanda BYOC" > staging-migration.yaml

# Production environment
claude-code "Create prod migration config: Confluent Cloud to Redpanda Cloud Dedicated with full schema migration" > prod-migration.yaml
```

---

## 🎓 Common Tasks

### Task 1: Schema Migration with Filtering

```bash
claude-code "Generate a migration config with schema subject filtering for 'orders.*' and 'users.*' patterns with normalization enabled" > schema-filtered.yaml
```

### Task 2: Cloud Migration

```bash
claude-code "Create a migration from Redpanda Dedicated to Serverless with consumer group exclusions and schema migration" > cloud-migration.yaml
```

### Task 3: Add Authentication

```bash
claude-code "Add SCRAM-SHA-256 authentication and TLS to my existing migration config" < base.yaml > authenticated.yaml
```

### Task 4: Optimize Configuration

```bash
claude-code "Review this migration config and suggest optimizations for faster topic discovery and schema sync" < current.yaml
```

---

## 🔍 Troubleshooting

### Skill Not Found

If Claude Code doesn't recognize the skill:

```bash
# Check skills directory
ls -la "$HOME/.claude-code/skills/"

# Verify redpanda-migrator exists
ls -la "$HOME/.claude-code/skills/redpanda-migrator/"

# Check SKILL.md is present
cat "$HOME/.claude-code/skills/redpanda-migrator/SKILL.md" | head -20
```

### Configuration Errors

```bash
# Validate generated configuration
python ~/.claude-code/skills/redpanda-migrator/scripts/validate_config.py config.yaml

# Check against example
diff config.yaml ~/.claude-code/skills/redpanda-migrator/assets/example-full-migration.yaml
```

### Getting Help

```bash
# Ask Claude Code for help
claude-code "What migration scenarios does the Redpanda Migrator skill support?"

# List available examples
claude-code "List all example configurations in the Redpanda Migrator skill"

# Explain specific option
claude-code "Explain the metadata_max_age configuration option"
```

---

## 📊 Skill Capabilities with Claude Code

When using Claude Code with the Redpanda Migrator skill, you can:

✅ **Generate configurations** from natural language descriptions
✅ **Validate YAMLs** using the included validation script
✅ **Reference examples** for common migration scenarios
✅ **Iterate quickly** on configurations with CLI commands
✅ **Access documentation** directly from the command line
✅ **Automate workflows** with shell scripts
✅ **Version control** your migration configurations

---

## 🚀 Advanced Integration

### Git Integration

```bash
# Initialize migration configs repository
mkdir migration-configs
cd migration-configs
git init

# Generate configurations
claude-code "Create migration configs for dev, staging, and prod" 

# Version control
git add *.yaml
git commit -m "Initial migration configurations"
```

### CI/CD Pipeline

```bash
# In your CI/CD pipeline
#!/bin/bash

# Generate config
claude-code "Create migration config from environment variables" > migration.yaml

# Validate
python ~/.claude-code/skills/redpanda-migrator/scripts/validate_config.py migration.yaml

# Deploy if valid
if [ $? -eq 0 ]; then
  kubectl apply -f migration-deployment.yaml
fi
```

### Scripted Generation

```bash
#!/bin/bash
# generate-migrations.sh

ENVIRONMENTS=("dev" "staging" "prod")

for env in "${ENVIRONMENTS[@]}"; do
  claude-code "Create $env environment migration config with appropriate settings" > "migration-${env}.yaml"
  echo "Generated migration-${env}.yaml"
done
```

---

## 📝 Environment Variables

Set these for easier access:

```bash
# Add to ~/.bashrc or ~/.zshrc
export CLAUDE_SKILLS_DIR="$HOME/.claude-code/skills"
export RP_MIGRATOR_SKILL="$CLAUDE_SKILLS_DIR/redpanda-migrator"
export RP_VALIDATE="python $RP_MIGRATOR_SKILL/scripts/validate_config.py"

# Aliases
alias rpvalidate="$RP_VALIDATE"
alias rpexamples="ls -la $RP_MIGRATOR_SKILL/assets/"
alias rpdocs="cat $RP_MIGRATOR_SKILL/SKILL.md | less"
```

---

## 🎯 Quick Start Commands

```bash
# 1. Install skill
unzip redpanda-migrator.skill -d ~/.claude-code/skills/redpanda-migrator

# 2. Generate your first config
claude-code "Create a basic Redpanda migration config" > my-migration.yaml

# 3. Validate it
python ~/.claude-code/skills/redpanda-migrator/scripts/validate_config.py my-migration.yaml

# 4. Run migration
rpk connect run my-migration.yaml
```

---

## 💡 Tips for Claude Code

1. **Be specific**: "Create a migration with SCRAM-SHA-256 auth, TLS, and schema normalization"
2. **Reference examples**: "Use the Confluent to Redpanda example as a base"
3. **Iterate**: Start simple, then add features incrementally
4. **Validate often**: Run validation after each generation
5. **Use examples**: Browse assets/ directory for patterns

---

## 📚 Additional Resources

- **Skill documentation**: `~/.claude-code/skills/redpanda-migrator/SKILL.md`
- **Configuration reference**: `~/.claude-code/skills/redpanda-migrator/references/config-spec.md`
- **Examples**: `~/.claude-code/skills/redpanda-migrator/assets/`
- **Validation script**: `~/.claude-code/skills/redpanda-migrator/scripts/validate_config.py`

---

## ✅ Verification

To verify the skill is working with Claude Code:

```bash
# Test skill recognition
claude-code "Does the Redpanda Migrator skill support Confluent Cloud migrations?"

# Expected: Claude Code should reference the skill and answer "Yes"

# Test configuration generation
claude-code "Generate a simple Redpanda migration config" > test.yaml

# Verify output is valid YAML
python -c "import yaml; yaml.safe_load(open('test.yaml'))"

# Clean up
rm test.yaml
```

---

## 🎉 You're Ready!

The Redpanda Migrator skill is now installed and ready to use with Claude Code. Start generating production-ready migration configurations from your terminal!

```bash
# Your first real migration config
claude-code "Create a production migration from Kafka to Redpanda Cloud with schemas, consumer offsets, and TLS authentication" > prod-migration.yaml
```

Happy migrating! 🚀
