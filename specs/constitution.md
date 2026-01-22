# Constitution
1. **Code Quality:** All Python code must be typed (using `typing` module) and documented.
2. **Architecture:** Separation of concerns. Even in a console app, separate the data logic (Service) from the input logic (UI).
3. **Testing:** All features must be verifiable.
4. **Event-Driven:** Systems should communicate asynchronously via events where possible, using Dapr for abstraction.
5. **Cloud-Native:** All components must be containerized, observable, and deployed via standard manifests (Helm).
6. **Infrastructure-as-Code:** All infrastructure (including secrets and config) must be defined in code (Helm, Terraform, or Scripts).