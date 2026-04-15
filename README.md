# File-Cleaner-
The HR Portal’s upload endpoint was exploited using a crafted filename with path traversal, allowing overwrite and defacing the homepage. After restoring the file, defenses were added: extension allowlist secure_filenamesanitization, and randomized UUIDbased storage names. This sandboxing prevents malicious overwrites and secures the application
