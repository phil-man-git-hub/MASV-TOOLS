# MASV Portal CLI

A command line tool to list, create, and delete MASV Portals.

## Installation

```bash
pip install masv_portal
```

## Configuration

Set the following environment variables:
- `MASV_API_KEY`: Your MASV API key
- `MASV_TEAM`: Your MASV team ID

## Usage

List portals:
```bash
masv_portal ls [IDsOrSubdomains...]
```

Create a new portal:
```bash
masv_portal new --subdomain <subdomain> --name <name> --message <message> --recipients <emails...>
```

Delete portals:
```bash
masv_portal rm <IDs...>
```

Use `--help` with any command for more information.