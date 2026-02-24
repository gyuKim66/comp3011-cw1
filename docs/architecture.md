# Architecture (DDD)

- Bounded contexts live in `backend/src/contexts/`
- Layers inside each context:
  - domain / application / infrastructure / interface
- Dependency rule:
  - interface → application → domain
  - infrastructure → domain
