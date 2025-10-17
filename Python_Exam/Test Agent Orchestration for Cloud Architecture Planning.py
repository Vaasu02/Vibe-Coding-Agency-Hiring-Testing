# Agent Orchestration for Cloud Architecture Planning
# Format: Problem statement + Written response

"""
AGENT ORCHESTRATION CHALLENGE

You need to design a multi-agent system that can analyze business problems and recommend 
cloud architecture solutions. Focus on the orchestration strategy, not implementation details.

SAMPLE SCENARIOS (choose 2 to address):

1. "Simple E-commerce Site"
   - Online store for small business (1000 daily users)
   - Product catalog, shopping cart, payment processing
   - Basic admin dashboard for inventory management

2. "Customer Support Chatbot"
   - AI chatbot for customer service 
   - Integration with existing CRM system
   - Handle 500+ conversations per day
   - Escalate complex issues to human agents

3. "Employee Expense Tracker"
   - Mobile app for expense reporting
   - Receipt photo upload and processing
   - Approval workflow for managers
   - Integration with payroll system

YOUR TASK:
Design an agent orchestration approach that can take these problems and output 
a cloud architecture recommendation including basic services needed (database, 
API gateway, compute, storage, etc.).
"""



# === WRITTEN RESPONSE QUESTIONS ===

"""
QUESTION 1: AGENT DESIGN (20 points)
What agents would you create for this orchestration? Describe:
- 3-5 specific agents and their roles
- How they would collaborate on the sample problems
- What each agent's input and output would be
"""
## QUESTION 1: AGENT DESIGN
AGENT_DESIGN_RESPONSE = """
## QUESTION 1: AGENT DESIGN

The orchestration uses a **Sequential/Pipeline Pattern** with five specialized agents:

1.  **Requirements Analyst (RA)**
    * **Role:** Decomposes the initial business problem into clear, quantifiable technical needs.
    * **Input:** Problem description (e.g., "Customer Support Chatbot").
    * **Output (JSON):** Functional Requirements (FRs), Non-Functional Requirements (NFRs) including load metrics (`load_conv_day: 500`), latency targets, and compliance requirements.

2.  **Data & Integration Agent (DIA)**
    * **Role:** Focuses on data types, storage strategy, and external system connectivity.
    * **Input:** Output from RA.
    * **Output (JSON):** Data storage recommendations (e.g., `db_type: NoSQL/Vector DB`), PII classification, and integration protocols (e.g., `integration_protocol: Async Queue`).

3.  **Compute & Infrastructure Agent (CIA)**
    * **Role:** Selects the most efficient compute model and infrastructure components based on the load and latency NFRs.
    * **Input:** Output from RA and DIA.
    * **Output (JSON):** Recommended compute model (e.g., `compute_model: Serverless Functions`), networking needs (e.g., API Gateway), and initial resource sizing estimates.

4.  **Security & Isolation Agent (SIA)**
    * **Role:** Designs the security architecture, including authentication, access control, and defense layers.
    * **Input:** Output from RA and DIA (especially PII classification).
    * **Output (JSON):** Required security services (e.g., WAF, Secrets Manager), authentication methods (e.g., OAuth), and compliance measures.

5.  **Resource Cost & Synthesis Agent (RCA)**
    * **Role:** Compiles all preceding outputs, validates the total architecture against NFRs, resolves conflicts, performs final cost estimation, and generates the report.
    * **Input:** Outputs from DIA, CIA, and SIA.
    * **Output:** Final structured architecture report (Markdown) with service list, cost estimate, and justification.
"""
# ---

"""
QUESTION 2: ORCHESTRATION WORKFLOW (25 points)
For ONE of the sample scenarios, walk through your complete workflow:
- Step-by-step process from problem statement to final recommendation
- How agents hand off information to each other
- What happens if an agent fails or produces unclear output
- How you ensure the final solution is complete and feasible
"""
## QUESTION 2: ORCHESTRATION WORKFLOW (Scenario: Customer Support Chatbot)
WORKFLOW_RESPONSE = """
## QUESTION 2: ORCHESTRATION WORKFLOW (Scenario: Customer Support Chatbot)

**Step-by-Step Workflow:**

1.  **Initiation (RA):** The Orchestrator sends the "Customer Support Chatbot" description to the **Requirements Analyst (RA)**. The RA decomposes it into **Load NFRs** (low-to-moderate, bursty, ~500 conv/day) and **Integration FRs** (CRM, Human Handoff).
2.  **Parallel Analysis (DIA, CIA, SIA):** The RA's output is immediately sent to the **Data & Integration Agent (DIA)**, **Compute & Infrastructure Agent (CIA)**, and **Security & Isolation Agent (SIA)**.
    * *CIA Decision:* Based on the bursty load NFR, the CIA selects **Serverless Functions** and **API Gateway**.
    * *DIA Decision:* Based on the integration FRs, the DIA mandates a **Queue Service** for decoupling CRM/Human Handoffs, and a **NoSQL/Vector DB** for scalable chat history.
    * *SIA Decision:* Based on the PII risk, the SIA requires a **WAF** for ingress protection and a **Secrets Manager** for CRM credentials.
3.  **Synthesis and Final Check (RCA):** The **Resource Cost & Synthesis Agent (RCA)** receives all three outputs.
    * **Validation:** RCA confirms the architecture supports all FRs (e.g., the Queue Service satisfies the Human Handoff requirement).
    * **Costing:** RCA estimates the monthly cost based on the chosen services and load NFRs.
4.  **Final Recommendation:** RCA outputs the completed, justified architecture report.

**Failure Handling and Feasibility:**

* **Handling Unclear Output:** If an agent (e.g., CIA) returns malformed JSON or an incomplete field, the Orchestrator runs a **Refinement Loop**. The Orchestrator resends the input to the failing agent along with a clear instruction: "The output was missing the required 'compute\_model' field. Re-run and ensure the JSON schema is strictly followed." This forces compliance before synthesis.
* **Ensuring Feasibility:** The RCA performs a final **Architectural Sanity Check**. It verifies that the combined services do not inherently conflict (e.g., a high-latency DB is not paired with a low-latency NFR). If a conflict exists (e.g., latency is too high), the RCA mediates by adding an appropriate service (like a Caching layer) and adjusting the TCO.
"""
# ---

"""
QUESTION 3: CLOUD RESOURCE MAPPING (20 points)
For your chosen scenario, what basic cloud services would your system recommend?
- Compute (serverless functions, containers, VMs)
- Storage (databases, file storage, caching)
- Networking (API gateways, load balancers, CDN)
- Security and monitoring basics
- Justify why each service fits the requirements
"""
## QUESTION 3: CLOUD RESOURCE MAPPING (Scenario: Customer Support Chatbot)
MAPPING_RESPONSE = """
## QUESTION 3: CLOUD RESOURCE MAPPING (Scenario: Customer Support Chatbot)

* **Compute:** **Serverless Functions** (e.g., AWS Lambda, Azure Functions)
    * **Justification:** The primary workload is event-driven (a new chat message). Serverless is ideal for **bursty, unpredictable traffic** and scales instantly while minimizing costs when idle.

* **Storage (Primary):** **Managed NoSQL/Vector DB** (e.g., DynamoDB, CosmosDB)
    * **Justification:** Provides the low-latency, high-scalability storage needed for chat logs (key-value access). The Vector index capability is essential for Retrieval-Augmented Generation (RAG) in modern AI chatbots.

* **Storage (Caching):** **In-memory Cache** (e.g., Redis)
    * **Justification:** Reduces latency for frequent state checks and short-term conversation context, helping meet the strict user-facing NFRs.

* **Networking:** **API Gateway**
    * **Justification:** Acts as the single, secured HTTP entry point for the mobile/web UI, providing rate limiting and seamless integration with the Serverless compute and WAF.

* **Integration/Messaging:** **Queue Service** (e.g., SQS, Service Bus)
    * **Justification:** Decouples the fast chat application from slower external systems like the CRM and human agent queues, ensuring the chat experience is not affected by downstream failures or latency.

* **Security:** **Web Application Firewall (WAF)**
    * **Justification:** Essential edge protection against common web exploits and, specifically for AI, against prompt injection attacks.

* **Security:** **Secrets Manager** (or Vault service)
    * **Justification:** Securely stores sensitive credentials (e.g., CRM API keys), injecting them into the compute environment at runtime using IAM roles, thereby avoiding hardcoded secrets.
"""
# ---

"""
QUESTION 4: REUSABILITY & IMPROVEMENT (15 points)
How would you make this system work across different projects?
- What would you standardize vs. customize per project?
- How would the system learn from previous recommendations?
- What feedback mechanisms would improve future solutions?
"""
## QUESTION 4: REUSABILITY & IMPROVEMENT
REUSABILITY_RESPONSE = """
## QUESTION 4: REUSABILITY & IMPROVEMENT

### Standardization vs. Customization
The **Agent Workflow and Interfaces** are standardized, while the **NFR values and Service Tiers** are customized.

* **Standardize (Fixed Components):**
    * The 5-agent pipeline (RA -> DIA/CIA/SIA -> RCA) and their specific JSON input/output schemas.
    * A minimum **Security Baseline** (e.g., IAM roles, PII encryption) enforced by the SIA for every project.
* **Customize (Variable Inputs):**
    * Target **Cloud Vendor** (AWS/Azure/GCP) and **Budget Tier** (Startup, Enterprise).
    * Specific **NFR Values** derived by the RA (e.g., `500ms` latency vs. `200ms` latency).

### Learning and Feedback Mechanisms

1.  **Human Overrides (The Core Learning Data):** The most valuable learning comes from **architectural changes** made *after* the RCA recommendation. If a human architect manually overrides the recommendation (e.g., rejects NoSQL and chooses Managed PostgreSQL, with the reason "Required for existing BI reporting tools"), this labeled delta is fed back into the RCA's model.
2.  **RCA Refinement Engine:** The **Resource Cost & Synthesis Agent (RCA)** is periodically fine-tuned on this dataset of successful and overridden recommendations. This teaches the RCA to adjust its conflict resolution logic—for instance, learning that when the word "Reporting" is a high-priority FR, it should preemptively favor relational databases despite higher cost.
3.  **Deployment Metrics:** Collecting and correlating actual runtime data (e.g., measured monthly cost vs. predicted cost; observed latency vs. NFR latency) from deployed solutions back to the RCA's initial predictions improves the accuracy of future cost estimates and service sizing.
"""
# ---

"""
QUESTION 5: PRACTICAL CONSIDERATIONS (20 points)
What challenges would you expect and how would you handle:
- Conflicting recommendations between agents
- Incomplete or vague problem statements
- Budget constraints not mentioned in requirements
- Integration with existing legacy systems
- Keeping up with new cloud services and pricing
"""
## QUESTION 5: PRACTICAL CONSIDERATIONS
PRACTICAL_RESPONSE = """
## QUESTION 5: PRACTICAL CONSIDERATIONS

* **Conflicting Recommendations:**
    * **Handling:** The **Resource Cost & Synthesis Agent (RCA)** is the single mediator with **Hierarchical Weighting**. Priority is strictly: **Security (SIA) > NFR Compliance (Latency/Load) > Cost**. If cost conflicts with latency NFR, latency wins, and the cost is documented.

* **Incomplete or Vague Problem Statements:**
    * **Handling:** The **Requirements Analyst (RA)** uses a mandatory validation check. If key NFRs (like expected max load or target latency) are missing, the RA will output a structured **Clarification Request** back to the user instead of proceeding, pausing the pipeline until the essential data is acquired.

* **Budget Constraints not mentioned:**
    * **Handling:** The RCA provides a **Tiered Recommendation Output**. It generates two full solutions: the **Performance Recommended** (meets all NFRs optimally, highest cost) and the **Cost-Optimized** (cheapest viable architecture, may slightly miss non-critical NFRs). This frames the cost vs. performance trade-off for the human architect.

* **Integration with existing legacy systems:**
    * **Handling:** The **Data & Integration Agent (DIA)** is trained to identify patterns for legacy integration. It is instructed to recommend implementing a robust **Queue/Broker (e.g., Kafka)** for guaranteed messaging, or an dedicated **Adapter Microservice** (often on Containers) to handle protocol translation and data scrubbing, isolating the modern architecture from legacy fragility.

* **Keeping up with new cloud services and pricing:**
    * **Handling:** The RCA is connected to a dynamic **Cloud Pricing API** (or database) that is updated daily. All agents are constrained to recommend **Managed Services First**, reducing reliance on rapidly changing low-level infrastructure specifics, thus making the architecture design more durable.
"""
# ---

# Combining the responses to complete the assignment file content.
FINAL_REPORT_TEXT = (
    AGENT_DESIGN_RESPONSE + "\n" +
    "---" + WORKFLOW_RESPONSE + "\n" +
    "---" + MAPPING_RESPONSE + "\n" +
    "---" + REUSABILITY_RESPONSE + "\n" +
    "---" + PRACTICAL_RESPONSE
)