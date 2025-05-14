class Entity {
  label string
  text string
  confidence float?
  language string?
}

function ExtractNER(text: string) -> Entity[] {
  client "openai/gpt-4o"
  prompt #"
    Extract named entities from the following resume text.

    Labels include:
    - SKILL (technologies, programming languages, methods)
    - PROJECT (personal or work-related projects)
    - ORG (companies or institutions)
    - CERTIFICATION (named credentials)
    - GPE (cities, countries)
    - PERSON (people names)
    - ACHIEVEMENT (awards, recognitions, accomplishments)

    Text:
    {{ text }}

    Answer in JSON format as a list of Entity objects.
    {{ ctx.output_format }}
  "#
}

// Batch research model
class EntityResearchResult {
  entity string
  summary string
}

// API for batch processing a list of entities
function ResearchEntities(entities: string[]) -> map<string, string> {
  client "openai/gpt-4o"
  prompt #"
    You are a named entities research assistant. For each entity below, return a concise summary of its meaning, significance, or context.
    This data will be used to enrich data for a recommendation letter composition.

    Entities:
    {{ entities }}

    Respond in JSON format:
    {
      "entity1": "summary1",
      "entity2": "summary2",
      ...
    }
  "#
}
