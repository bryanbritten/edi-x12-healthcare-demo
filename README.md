# EDI X12 Healthcare Pipeline

This project simulates an end-to-end EDI ingestion and processing pipeline designed for healthcare X12 data (e.g., 837, 835, 834, 999, 277). It models a realistic enterprise data integration flow using Python components to simulate the behavior of traditional tools such as Mirth Connect, Boomi, or MuleSoft, without relying on external commercial software.

## Overview

The pipeline ingests EDI files from a mock SFTP server, validates and parses them, performs data quality checks, and routes the results to appropriate storage targets in a simulated cloud environment (mock S3 buckets). Metrics, logging, and alerting are included for observability and debugging purposes.

## Workflow Summary

1. **Message Repository**  
   A repository of example X12 messages (provided by [x12.org](https://x12.org/examples)) is maintained as input for the pipeline.

2. **Invalidator**  
   A configurable process randomly corrupts a subset of the X12 messages to simulate real-world transmission issues or malformed files.

3. **SFTP Drop**  
   Corrupted and clean messages are dropped into a mock SFTP server for downstream consumption.

4. **Mock EDI Ingestor**  
   A Python-based batch ingestor mimics the behavior of a commercial integration engine. It pulls files from the SFTP location on a schedule or trigger.

5. **Parsing and Validation**  
   - Messages are parsed using an X12 parser (custom or library-based).
   - Schema validation is performed (segment order, required fields, control numbers, etc.).
   - Business-level data quality checks ensure referential and content accuracy.

6. **Routing Logic**  
   - Messages that fail parsing, validation, or data QA are moved to a `deadletter` bucket for inspection.
   - Clean messages are written to the `silver` bucket in mock S3 (cleaned, structured, ready for downstream use).

7. **Observability**
   - **Logging** captures pipeline activity and errors.
   - **Metrics** track ingest volume, failure counts, and throughput rates.
   - **Alerting** (optional) can be triggered on failure thresholds or ingest timeouts.

## Message Types Supported

- `837P` / `837I` / `837D` – Health Care Claims
- `835` – Payment Remittance Advice
- `834` – Benefit Enrollment and Maintenance
- `999` – Functional Acknowledgment
- `277CA` – Claim Acknowledgment

## Buckets

- `sftp/` – Input drop location for X12 messages
- `bronze/` - Raw, unprocessed, non-validated X12 messages
- `silver/` – Successfully parsed and validated X12 content
- `deadletter/` – Failed messages for manual inspection

## Error Types

- **Parsing Error** – Malformed structure, delimiters, or control segments
- **Validation Error** – Schema-level failures (e.g., missing segments)
- **Quality Error** – Business logic violations (e.g., invalid codes, date mismatches)

## Metrics Tracked

- `messages_processed_total`
- `messages_failed_parse`
- `messages_failed_validation`
- `messages_failed_quality`
- `messages_successful`
- `average_processing_latency`

## Dependencies

- Python 3.12+
- Libraries:
  - `pysftp` or `paramiko` (TBD) for SFTP simulation
  - `boto3` or file mocks for S3 simulation
  - `x12` or `bots` (TBD)
  - `prometheus_client` for metrics exposure
  - `logging` for logs

## Notes

- This is a simulation project intended for learning and prototyping.
- No PHI or real data was (nor should be) used.
- Integration with real EDI VANs or production SFTP servers is out of scope.
