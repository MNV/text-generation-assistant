// Define the function to generate a personalized recommendation letter
function GenerateRecommendationLetter(
  principal_facts: Resume,
  grantee_facts: Resume,
  principal_context: string,
  grantee_context: string,
  recommendation_type: string,
  directives: string,
  circumstances: string,
  entity_research: map<string, string>,
  few_shot_examples: string,
  extra: map<string, string>,
) -> string {
  client "openai/gpt-4o"
  prompt #"
    You are a professional academic advisor writing a formal recommendation letter.

    Below are example letters to help guide tone and style:
    {{ few_shot_examples }}

    Task:
    Write a recommendation letter for the purpose of: {{ recommendation_type }}.

    Recommender (Principal) information:
    {% if principal_facts.name %}
        Name: {{ principal_facts.name }}
    {% endif %}
    {% if principal_facts.email %}
        Email: {{ principal_facts.email }}
    {% endif %}
    {% if principal_facts.location %}
        Location: {{ principal_facts.location }}
    {% endif %}
    {% if principal_facts.summary %}
        Summary: {{ principal_facts.summary }}
    {% endif %}
    {% if principal_facts.experience %}
        Experience:
        {% for exp in principal_facts.experience %}
            - {{ exp.job_title }} at {{ exp.company }} ({{ exp.start_date }} – {{ exp.end_date }})
                Responsibilities: {{ exp.responsibilities | join(", ") }}
        {% endfor %}
    {% endif %}

    Additional Context about Recommender:
    {{ principal_context }}

    Candidate (Grantee) information:
    {% if grantee_facts.name %}
        Name: {{ grantee_facts.name }}
    {% endif %}
    {% if grantee_facts.location %}
        Location: {{ grantee_facts.location }}
    {% endif %}
    {% if grantee_facts.summary %}
        Summary: {{ grantee_facts.summary }}
    {% endif %}
    {% if grantee_facts.experience %}
        Experience:
        {% for exp in grantee_facts.experience %}
            - {{ exp.job_title }} at {{ exp.company }} ({{ exp.start_date }} – {{ exp.end_date }})
                Responsibilities: {{ exp.responsibilities | join(", ") }}
        {% endfor %}
    {% endif %}

    Additional Context about Candidate:
    {{ grantee_context }}

    Circumstances under which the candidate and recommender met: {{ circumstances }}

    Context to highlight in the letter:
    {% for entry in entity_research %}- {{ entry }}: {{ entity_research[entry] }}
    {% endfor %}

    Additional Instructions:
    {{ directives }}

    Please generate a formal, fluent, and logically structured recommendation letter that highlights the candidate's strengths and reflects the context of their relationship with the recommender. Adapt the tone and emphasis according to the recommendation type.
    Replace all the placeholders with principal and grantee data where applicable. The letter must be fully completed.
    It must not have raw placeholders (fill them with accordingly):
        [Your Name] – use principal full name.
        [Your Address] – use principal location data.
        [City, State, ZIP Code] – use principal location data.
        [Email Address] – use principal email.
        [Date] – use date {{ extra.current_date }}, but reformat it and integrate into recommendation letter design

    Translate all the Russian text to English (including names and titles).
    Do not include "Attachments" section, but only well formatted recommendation letter text.

    Response:
    {{ ctx.output_format }}
  "#
}
