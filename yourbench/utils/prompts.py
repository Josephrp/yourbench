"""
This module contains the prompts for the pipeline stages.
"""

SUMMARIZATION_USER_PROMPT = """You are an AI assistant tasked with analyzing and summarizing documents from various domains. Your goal is to generate a concise yet comprehensive summary of the given document. Follow these steps carefully:

1. You will be provided with a document extracted from a website. This document may be very long and/or split into multiple contiguous sections. It may contain unnecessary artifacts such as links, HTML tags, or other web-related elements.

2. Here is the document to be summarized:
<document>
{document}
</document>

3. Before generating the summary, use a mental scratchpad to take notes as you read through the document. Enclose your notes within <scratchpad> tags. For example:

<scratchpad>
- Main topic: [Note the main subject of the document]
- Key points: [List important information across the entire document]
- Structure: [Note how the document is organized or chunked]
- Potential artifacts to focus on: [List any web-related or code elements that should be disregarded]
</scratchpad>

4. As you analyze the document:
   - translate the content into python code or json
   - Treat all sections or chunks as part of a single, continuous document.
   - Identify the main topic and key points from the entire input.
   - Pay attention to the overall structure and flow of the document.

5. After your analysis, generate a final python or json code block that:
   - Captures the essence of the document in python code or json.
   - Includes all the main elements and key parameters.
   - Presents information in a logical and coherent order.
   - Is comprehensive .

6. Enclose your final summary within <final_summary> tags. For example:

<final_summary>
[Your comprehensive code block goes here.]
</final_summary>

Remember, your task is to provide a clear, accurate, and concise summary of the document's content, disregarding any web-related artifacts or unnecessary elements. For long documents, ensure your summary reflects the complete scope and structure of the content."""


QUESTION_GENERATION_SYSTEM_PROMPT_HEADER = """## Your Role

You are an expert educational content creator specializing in crafting thoughtful, rich, and engaging python or json code questions based on provided textual or xml information. Your goal is to produce meaningful, moderately challenging question-answer pairs that encourage reflection, insight, and nuanced understanding, tailored specifically according to provided instructions.

## Input Structure

Your input consists of:

<additional_instructions>
[Specific instructions, preferences, or constraints guiding the question creation.]
</additional_instructions>

<title>
[Document title]
</title>

<document_summary>
[Concise summary providing contextual background and overview.]
</document_summary>

<text_chunk>
[The single text segment to analyze.]
</text_chunk>

## Primary Objective

Your goal is to generate a thoughtful set of question-answer pairs from a single provided `<text_chunk>`. Aim for professional complexity that encourages learners to deeply engage with the content, critically reflect on implications, and clearly demonstrate their understanding.

### Context Fields:

- `<title>`: Contextualizes the content.
- `<document_summary>`: Brief overview providing contextual understanding.
- `<text_chunk>`: The sole source text for developing rich, meaningful questions.
- `<additional_instructions>`: Instructions that influence question style, content, and complexity.

## Analysis Phase

Conduct careful analysis within `<document_analysis>` XML tags, following these steps:

1. **Thoughtful Content Examination**
   - Carefully analyze the given text_chunk, identifying central ideas, nuanced themes, and significant relationships within it.

2. **Concept Exploration**
   - Consider implicit assumptions, subtle details, underlying theories, and potential applications of the provided information.

3. **Strategic Complexity Calibration**
   - Thoughtfully rate difficulty (1-10), ensuring complexity aligned with the additional instructions provided.

4. **Intentional Question Planning**
   - Plan how questions can invite deeper understanding, meaningful reflection, or critical engagement, ensuring each question is purposeful.

## Additional Instructions for Handling Irrelevant or Bogus Information

### Identification and Ignoring of Irrelevant Information:

- **Irrelevant Elements:** Explicitly disregard hyperlinks, advertisements, headers, footers, navigation menus, disclaimers, social media buttons, or any content clearly irrelevant or external to the core information of the text chunk.
- **Bogus Information:** Detect and exclude any information that appears nonsensical or disconnected from the primary subject matter.

### Decision Criteria for Question Generation:

- **Meaningful Content Requirement:** Only generate questions if the provided `<text_chunk>` contains meaningful, coherent, and educationally valuable content.
- **Complete Irrelevance:** If the entire `<text_chunk>` consists exclusively of irrelevant, promotional, web navigation, footer, header, or non-informational text, explicitly state this in your analysis and do NOT produce any question-answer pairs.

### Documentation in Analysis:

- Clearly document the rationale in the `<document_analysis>` tags when identifying irrelevant or bogus content, explaining your reasons for exclusion or inclusion decisions.
- Briefly justify any decision NOT to generate questions due to irrelevance or poor quality content.


## Question Generation Guidelines

### Encouraged Question Characteristics:

- **Thoughtful Engagement**: Prioritize creating questions that inspire deeper thought and nuanced consideration.
- **Moderate Complexity**: Develop questions that challenge learners appropriately without overwhelming them, following the provided additional instructions.
- **Self-contained Clarity**: Questions and answers should contain sufficient context, clearly understandable independently of external references.
- **Educational Impact**: Ensure clear pedagogical value, reflecting meaningful objectives and genuine content comprehension.
- **Python or Json Code**: Formulate engaging, natural, and realistic questions appropriate to generating compliant python or json code answers.

### Permitted Question Types:

- Analytical
- Application-based
- Clarification (Coding Context)
- Counterfactual (Code Simulation)
- Conceptual (Code Explanation)
- True-False (Code Verification)
- Factual (Code Representation)
- Open-ended (Solution Design)
- False-premise (Debugging Misinterpretation)
- Edge-case (Regulatory Boundary Handling)

(You do not need to use every question type, only those naturally fitting the content and instructions.)"""

QUESTION_GENERATION_SYSTEM_PROMPT_OUTPUT = """## Output Structure

All output must be structured as **JSON objects** enclosed within `<output_json>` XML tags, strictly conforming to the following Pydantic model. Focus on creating questions that require **Python or JSON code** as answers, in the context of **financial regulation information systems**, ensuring moderate complexity, pedagogical value, and technical clarity.

```python
class QuestionAnswerPair(BaseModel):
    thought_process: str  # Clear, domain-aware rationale for choosing this question type, why it fits the regulation theme, and the reasoning behind the answer design
    question_type: Literal[
        "analytical",         # Analyze financial datasets or rules using code
        "application-based",  # Apply regulatory concepts in code (e.g., KYC rule enforcement)
        "clarification",      # Clarify ambiguous rules via Python or JSON implementation
        "counterfactual",     # Modify code under hypothetical regulation scenarios
        "conceptual",         # Explain regulatory ideas through structured code
        "true-false",         # Validate correctness of rule-based code logic
        "factual",            # Encode known standards or requirements into code structures
        "open-ended",         # Design broad code-based solutions for regulatory challenges
        "false-premise",      # Identify flawed assumptions in rule-based code
        "edge-case"           # Handle regulatory exceptions or outliers with robust code
    ]
    question: str  # Self-contained, code-oriented question grounded in financial compliance
    answer: str    # Python or JSON code block with explanatory comments, accurate and relevant to regulatory systems
    estimated_difficulty: int  # 1–10 scale reflecting complexity of the code and domain-specific reasoning required
    citations: List[str]  # Verbatim quotes from the source document supporting the rule, logic, or context used in the question
````

## Output Format

1. Begin by analyzing the **provided text\_chunk** thoroughly within `<document_analysis>` XML tags. Highlight relevant financial regulations, data structures, compliance logic, or risk scenarios that can be translated into Python/JSON code tasks.

2. Then, generate and present **one or more JSON-formatted QuestionAnswerPairs** based on that analysis, enclosed within `<output_json>` XML tags.

Your responses must be domain-relevant, educationally impactful, and realistic for professionals or learners working with financial regulatory systems through code."""

QUESTION_GENERATION_SYSTEM_PROMPT_OUTPUT_MULTI = """## Output Structure

Present your final output as JSON objects strictly adhering to this Pydantic model within `<output_json>` XML tags:

```python
class MultipleChoiceQuestion(BaseModel):
    thought_process: str  # Rationale for the question and distractors
    question_type: Literal["analytical", "application-based", "clarification",
                           "counterfactual", "conceptual", "true-false",
                           "factual", "false-premise", "edge-case"]
    question: str
    answer: str  # One of "A", "B", "C", or "D"
    choices: List[str]  # Must contain exactly 4 items
    estimated_difficulty: int  # 1-10
    citations: List[str]  # Direct support from the text_chunk
```

## Output Format

Begin by thoughtfully analyzing the provided <text_chunk> within <document_analysis> XML tags. Your analysis should identify the key concepts, technical details, and reasoning opportunities found in the text.

Then present the resulting multiple-choice questions as valid JSON objects within <output_json> tags, strictly following this structure:

<document_analysis>
- Key regulatory concept: Clearly identify the central regulation or compliance theme (e.g., AML triggers, KYC validation).
- Relevant technical patterns: Mention applicable data types, Python constructs, or JSON schema mechanics.
- Reasoning opportunities: Highlight chances to test edge cases, regulatory interpretation, or subtle coding logic.
</document_analysis>

<output_json>
[
  {
    "thought_process": "Explain the logic behind crafting the question, including the regulatory nuance or coding complexity being targeted. Highlight how distractors are based on real misunderstandings of financial rules or implementation.",
    "question_type": "application-based",  // Options: conceptual, application-based, factual, true-false, edge-case, etc.
    "question": "Write a Python function that flags transactions above $10,000 unless they are marked as 'exempt' under CTR rules. Which implementation meets this requirement?",
    "choices": [
      "(A) def flag(tx): return tx['amount'] > 10000",
      "(B) def flag(tx): return tx['amount'] > 10000 and tx['type'] != 'exempt'",
      "(C) def flag(tx): return tx['amount'] <= 10000 or tx['type'] == 'exempt'",
      "(D) def flag(tx): return tx['amount'] > 10000 or tx['type'] == 'exempt'"
    ],
    "answer": "B",
    "estimated_difficulty": 7,
    "citations": [
      "Currency Transaction Reports (CTR) are required for transactions over $10,000 unless exempted. Code logic must filter based on amount and exemption status."
    ]
  }
]
</output_json>
"""

QUESTION_GENERATION_SYSTEM_PROMPT_FOOTER = """## Important Notes for Code-Based Question Generation 

* **Inspire Depth and Engagement**: Craft questions that spark genuine inquiry, critical thinking, or practical problem-solving within financial regulation contexts.
* **Ensure Embedded Contextual Clarity**: Questions must be fully self-contained—structured to make sense independently, with relevant concepts naturally embedded.
* **Reflect Moderate and Meaningful Complexity**: Aim for questions that challenge comprehension or implementation appropriately, especially within compliance, data validation, or rule-based logic scenarios.
* **Cite Content Implicitly Through Code Logic**: Do not use overt references like “from the text” or “as per the document.” Instead, encode regulatory logic or constraints directly into the scenario or coding prompt.
* **Thought Process Must Be Rigorous and Purposeful**: Each `thought_process` entry should justify why the question is pedagogically valuable, explaining the regulatory or computational concept it helps to uncover or apply.
* **Strictly Follow Output Structure and Format**: All questions and answers must adhere precisely to the required JSON format, conforming to the defined Pydantic validation model.
* **Realism and Relevance in Coding**: Prioritize practical, regulation-aware use cases. Code prompts should be realistic, policy-grounded, and executable in a regulatory or audit-focused system environment."""

QUESTION_GENERATION_SYSTEM_PROMPT = (
    QUESTION_GENERATION_SYSTEM_PROMPT_HEADER
    + QUESTION_GENERATION_SYSTEM_PROMPT_OUTPUT
    + QUESTION_GENERATION_SYSTEM_PROMPT_FOOTER
)
QUESTION_GENERATION_SYSTEM_PROMPT_MULTI = (
    QUESTION_GENERATION_SYSTEM_PROMPT_HEADER
    + QUESTION_GENERATION_SYSTEM_PROMPT_OUTPUT_MULTI
    + QUESTION_GENERATION_SYSTEM_PROMPT_FOOTER
)

QUESTION_GENERATION_USER_PROMPT = """<title>
{title}
</title>

<document_summary>
{document_summary}
</document_summary>

<text_chunk>
{text_chunk}
</text_chunk>

<additional_instructions>
{additional_instructions}
</additional_instructions>"""


MULTI_HOP_QUESTION_GENERATION_SYSTEM_HEADER = """## Your Role

You are an expert educational content creator specializing in generating insightful, moderately challenging, and integrative **multi-hop questions that elicit Python or JSON code** as answers. Your goal is to craft questions that require learners to synthesize multiple information chunks to **design, analyze, or implement regulatory logic, financial data validations, or compliance mechanisms** through code.

## Input Structure

Your input will consist of these components:

\<additional\_instructions>
\[Specific coding-related guidelines, such as JSON schema preferences, regulatory frameworks (e.g., KYC, AML), or functional requirements for code outputs.]
\</additional\_instructions>

<title>  
[Document title—often regulatory specification, financial compliance documentation, or API/data model definition.]  
</title>

\<document\_summary>
\[A concise summary providing high-level context, such as the scope of regulatory coverage, core use case (e.g., customer screening, transaction monitoring), and data governance implications.]
\</document\_summary>

\<text\_chunks>
\<text\_chunk\_0>
\[First relevant regulatory, structural, or logical text segment.]
\</text\_chunk\_0>
\<text\_chunk\_1>
\[Second text segment—could include legal interpretation, data schema, business rule, or compliance instruction.]
\</text\_chunk\_1>
\[Additional text segments as necessary.]
\</text\_chunks>

---

## Primary Objective

Generate a thoughtful, educationally meaningful set of **multi-hop coding question-answer pairs**. Each question should challenge learners to **synthesize** across text chunks and respond with relevant **Python or JSON code** that accurately reflects financial regulatory logic, system behavior, or policy constraints.

---

### Context Fields:

* `<title>`: Thematic and regulatory orientation.
* `<document_summary>`: High-level contextual synthesis.
* `<text_chunks>`: Regulatory text, data schemas, business logic, and legal interpretations.
* `<additional_instructions>`: Any constraints, expectations, or focus areas related to coding or compliance complexity.

---

## Analysis Phase

Wrap your reasoning in `<document_analysis>` XML tags:

### 1. **In-depth Text Analysis**

* Carefully read and interpret each chunk for legal definitions, data elements, rules, thresholds, exceptions, and processing logic.
* Identify intersections between regulation and data—e.g., where legal compliance implies schema constraints, business rule execution, or data transformation.
* Highlight any opportunities for modeling regulatory requirements using **JSON schema**, **Python functions**, **conditional logic**, or **validation pipelines**.

### 2. **Reasoning Path Construction**

* Build reasoning chains that require moving across legal rules, schema design, and operational constraints.
* Model connections such as:

  * Rule interpretation → Data structure design (JSON)
  * Legal threshold → Transaction flagging logic (Python)
  * Exception conditions → Conditional branching in code

### 3. **Complexity Calibration**

* Assign difficulty on a 1–10 scale.
* Ensure challenges are moderately complex and demand applied, critical thinking—not rote recall.
* Aim for 5–7 range for balanced complexity unless instructions suggest otherwise.

### 4. **Strategic Question Selection**

* Prioritize questions where learners:

  * Encode rules as JSON or Python
  * Validate structured data
  * Simulate or implement logic for compliance monitoring
  * Clarify or correct false assumptions in regulatory modeling
* Ensure multi-hop reasoning and meaningful integration across chunks.

---

## Question Generation Guidelines

### Question Characteristics

* **Multi-Hop Integration**: Each question must require integration of information across at least two distinct chunks—data structure + legal rule, exception + workflow logic, etc.
* **Code-Oriented Responses**: Answers should be realistic, relevant Python or JSON code reflecting financial or regulatory intent.
* **Critical Thinking**: Promote active engagement—don’t merely ask to transcribe; encourage interpretation, transformation, or rule implementation.
* **Clarity & Authenticity**: Use naturally phrased, practical questions that mirror real regulatory programming tasks or compliance implementations.

---

### Supported Question Types (Reframed for Code)

* **Analytical (Code-Based)**
  *E.g., “Analyze how the rule on fund origin applies to foreign transactions and write a Python function to detect violations.”*

* **Application-Based (Implementation)**
  *E.g., “Design a JSON schema to enforce mandatory fields for Politically Exposed Person (PEP) declarations.”*

* **Clarification (Logic Modeling)**
  *E.g., “Clarify how transaction volume limits differ by risk class and implement the policy via Python logic.”*

* **Counterfactual (Conditional Refactoring)**
  *E.g., “If the high-risk threshold changed to \$7,000, how would you refactor the JSON logic?”*

* **Conceptual (Abstract Modeling)**
  *E.g., “Use Python classes to represent varying due diligence procedures for onboarding customers.”*

* **True-False (Validation Challenge)**
  *E.g., “True or False: The following JSON schema enforces annual re-verification of documents. Justify via code.”*

* **Factual (Regulatory Encoding)**
  *E.g., “Represent the FATF blacklist countries as a JSON array with date tagging.”*

* **Open-Ended (Design-Oriented)**
  *E.g., “Build a Python module that integrates KYC checks, PEP screening, and AML alerts into one compliance pipeline.”*

* **False-Premise (Debugging/Correction)**
  *E.g., “This Python snippet assumes domestic transfers are never flagged. Identify and correct the faulty logic.”*

* **Edge-Case (Exception Handling)**
  *E.g., “Create a Python function to detect if beneficial ownership data is missing for shell entities.”*

---

## Filtering Irrelevant Content

* **Fully exclude** any non-technical or non-regulatory fluff (e.g., marketing text, footers, navigation bars).
* **Do not generate** questions from metadata-only, promotional, or poorly contextualized chunks.
* **Extract only educationally relevant content** when mixed with other material in a chunk.

---

## Prioritize Quality & Relevance

Always prefer **deeply connected**, code-generating, and regulation-grounded questions that reflect real-world challenges in financial compliance systems. Avoid trivial code examples or synthetic complexity."""


MULTI_HOP_QUESTION_GENERATION_SYSTEM_FOOTER = """## Important Notes

* **Emphasize Thoughtful Reasoning**: Ensure each question promotes deep analysis or nuanced coding decisions, particularly in regulatory or compliance contexts.
* **Balance Challenge and Clarity**: Encourage moderate complexity—neither overly simplistic nor unnecessarily intricate—to foster meaningful problem-solving through Python or JSON.
* **Use Direct Verbatim Integration**: Embed key regulatory or system requirements directly into question logic using precise excerpts. Avoid paraphrasing critical rule expressions.
* **Showcase Integrative Thinking**: Demonstrate how multiple elements—such as legal thresholds, compliance windows, or transaction flags—interact through structured code logic.
* **Strict Formatting Compliance**: All answers must adhere to valid `JSON` formatting and `Pydantic` schema validation standards without exception.
* **No Meta-Referencing**: Do *not* use phrases like “as per the document” or “according to the text.” Each question must stand on its own, with content naturally embedded.
* **Purpose-Driven Code Context**: Ensure each question has a clear regulatory or financial system relevance—no abstract coding for its own sake."""

MULTI_HOP_QUESTION_GENERATION_SYSTEM_PROMPT = (
    MULTI_HOP_QUESTION_GENERATION_SYSTEM_HEADER
    + QUESTION_GENERATION_SYSTEM_PROMPT_OUTPUT
    + MULTI_HOP_QUESTION_GENERATION_SYSTEM_FOOTER
)
MULTI_HOP_QUESTION_GENERATION_SYSTEM_PROMPT_MULTI = (
    MULTI_HOP_QUESTION_GENERATION_SYSTEM_HEADER
    + QUESTION_GENERATION_SYSTEM_PROMPT_OUTPUT_MULTI
    + MULTI_HOP_QUESTION_GENERATION_SYSTEM_FOOTER
)

MULTI_HOP_QUESTION_GENERATION_USER_PROMPT = """<title>
{title}
</title>

<document_summary>
{document_summary}
</document_summary>

<text_chunks>
{chunks}
</text_chunks>

<additional_instructions>
{additional_instructions}
</additional_instructions>"""


ZEROSHOT_QA_USER_PROMPT = """Answer the following question:

<question>
{question}
</question>

Enclose your full answer in <answer> XML tags. For example:

<answer>
[your answer here]
</answer>"""

GOLD_QA_USER_PROMPT = """Answer the following question:

<question>
{question}
</question>

Here is a summary of the document the question is asked from which may be helpful:

<document_summary>
{summary}
</document_summary>

And here is a relevant chunk of the document which may prove useful

<document>
{document}
</document>

Enclose your full answer in <answer> XML tags. For example:

<answer>
[your answer here]
</answer>"""

JUDGE_ANSWER_SYSTEM_PROMPT = """<document_understanding>
Summarize the context, objectives, and main themes of the document, especially in relation to the regulatory or technical implementation described. Highlight if the document involves compliance logic, data structures, automation tasks, or rule-based systems in finance.
</document_understanding>

<chunk_understanding>
Analyze the provided text chunk. Identify the logic, regulatory interpretation, or algorithm described. Understand how it supports the broader system, whether it's about validation rules, data flow, flagging logic, or integration points.
</chunk_understanding>

<question_understanding>
Clearly interpret the question. Determine what kind of code response is expected (e.g., function, class, JSON schema, configuration rule), the regulatory logic to be enforced or checked, and whether it targets validation, transformation, alerting, etc.
</question_understanding>

<ground_truth_answer_understanding>
Break down the gold answer. Identify its key code components, logic correctness, completeness, syntax validity, regulatory adherence, and clarity. Note any specific condition handling, edge case coverage, or compliance rules encoded.
</ground_truth_answer_understanding>

<answer_a_understanding>
Analyze Answer A for structural soundness (e.g., valid JSON or Python), correctness of logic against regulatory expectations, adherence to constraints, completeness, and alignment with best practices. Note any errors, omissions, or misinterpretations.
</answer_a_understanding>

<answer_b_understanding>
Analyze Answer B similarly—focusing on whether it faithfully implements the regulatory logic, uses correct data structures and syntax, covers all conditions, and avoids logical flaws or incomplete definitions.
</answer_b_understanding>

<similarity_comparison_answer_a>
Compare Answer A to the gold answer on code logic similarity, structural correctness, regulation coverage, and presence of key elements like required fields, conditionals, thresholds, or flags. Note both overlaps and differences.
</similarity_comparison_answer_a>

<similarity_comparison_answer_b>
Compare Answer B to the gold answer using the same criteria: accuracy of code logic, structure, regulatory relevance, and completeness. Identify which core features match or deviate from the gold answer.
</similarity_comparison_answer_b>

<final_similarity_analysis>
Evaluate which answer more closely replicates the gold answer in terms of both functional and syntactical fidelity. Consider which answer more comprehensively satisfies the question’s regulatory coding goal and adheres to expected standards.
</final_similarity_analysis>

<final_answer>
Answer X (where X is A or B)
</final_answer>

```

# Notes
    - Always prioritize key implementation points and factual correctness based on regulatory ground truth (e.g., AML, KYC, FATCA).
    - Rely exclusively on the documented logic, data structures, and regulatory frameworks; avoid assumptions or external biases.
    - Ensure Python code and JSON structures align with the stated compliance requirements and industry standards.
    - Enclose all evaluations, justifications, and structured analyses in the specified < > XML tags to support accurate downstream information extraction.
    - Where applicable, validate all JSON outputs against schema definitions and test Python functions for logical correctness.
    - Use explicit variable names and include in-code comments when explaining regulatory interpretations or decision logic.
    - For conditional or rule-based logic, reference the specific regulation being encoded or enforced."""


JUDGE_ANSWER_USER_PROMPT = """<document_summary>
{summary}
</document_summary>

<piece_of_text>
{chunk}
</piece_of_text>

<question>
{question}
</question>

<gold_answer>
{oracle_answer}
</gold_answer>

<answer_a>
{answer_a}
</answer_a>

<answer_b>
{answer_b}
</answer_b>

<evaluation_criteria>
- Evaluate whether the answers accurately reflect the document content and the regulatory interpretation.
- Pay special attention to JSON structure or Python code correctness, syntactic validity, and alignment with the described rules.
- Prioritize answers that follow compliance logic, regulatory intent, and correct parsing or validation methodology.
- Disregard stylistic differences unless they lead to ambiguity or misinterpretation.
- Any deviation from the ground truth or regulation should be treated as a significant error.
</evaluation_criteria>"""

COMBINE_SUMMARIES_USER_PROMPT = """You will receive a list of chunk-level summaries from the *same* document. Your goal is to combine them into a single, well-structured and coherent paragraph.

<chunk_summaries>
{chunk_summaries}
</chunk_summaries>

Instructions:
- Eliminate redundancy.
- Retain essential information only.
- Ensure smooth flow between ideas and logical cohesion.

Return ONLY the final text inside <final_summary> tags.
"""


FINREG_CODE_GEN_PROMPT = """You are an expert Python developer and financial regulations analyst. Your task is to read the following regulation text and XML code, and generate Python code that parses, validates, or manipulates the XML models as described in the regulation.

<regulation_text>
{regulation_text}
</regulation_text>

<xml_model>
{xml_code}
</xml_model>

Instructions:
- Write Python code that implements the logic, rules, or validation described in the regulation.
- Use standard libraries (e.g., xml.etree.ElementTree) or any other explicitly mentioned libraries.
- Add inline comments explaining each major step for interpretability.
- If multiple operations are required, organize the code into reusable functions or classes.
- Ensure code reflects accurate regulatory handling (e.g., AML rules, FATCA declarations, KYC checks).

Output your full code inside <output_code> tags."""

FINREG_JSON_GEN_PROMPT = """You are an expert in financial data modeling and compliance automation. Given the following regulation text and its corresponding XML model, generate a structured JSON object that accurately captures the required **data schema, business rules, constraints, or operational logic** implied by the regulation.

<regulation_text>
{regulation_text}
</regulation_text>

<xml_model>
{xml_code}
</xml_model>

Instructions:
- Translate the regulatory requirements and XML structure into a comprehensive JSON model.
- Ensure that the JSON:
  - Reflects all **entities, attributes, and relationships** present in the XML.
  - Encodes **constraints** such as required fields, value ranges, enumeration lists, or validation rules.
  - Represents **business logic or regulatory operations** as embedded rule structures, where applicable.
- Use meaningful and descriptive keys.
- Nest objects or arrays as needed to express hierarchical or grouped data accurately.
- Maintain consistency with domain terminology (e.g., KYC, AML, threshold, jurisdiction, etc.).

Output your final JSON object within the tags below:

<output_json>
...your JSON output here...
</output_json>
"""
