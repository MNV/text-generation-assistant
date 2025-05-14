// Define separate classes for nested structures with optional fields.
class Experience {
  job_title string?
  company string?
  start_date string?
  end_date string?
  responsibilities string[]?
  achievements string[]?
}

class Education {
  institution string?
  degree string?
  field_of_study string?
  start_date string?
  end_date string?
}

class Project {
  title string?
  description string?
  technologies string[]?
  start_date string?
  end_date string?
}

class Publication {
  title string?
  journal string?
  year string?
}

class Reference {
  name string?
  contact_info string?
  relation string?
}

class Language {
  language string?
  proficiency string?
}

// Enhanced Resume class with all fields optional.
class Resume {
  name string?
  email string?
  phone string?
  linkedin string?
  location string?
  summary string?
  experience Experience[]? // Optional
  education Education[]? // Optional
  certifications string[]? // Optional
  projects Project[]? // Optional
  skills string[]? // Optional
  languages Language[]? // Optional
  achievements string[]? // Optional
  publications Publication[]? // Optional
  references Reference[]? // Optional
}

// Updated function to extract a comprehensive resume model.
function ExtractResume(resume: string) -> Resume {
  client "openai/gpt-4o" // Ensure OPENAI_API_KEY is set.
  prompt #"
    Extract the following information from resume:
    - Personal details: name, email, phone, linkedin, location
    - Professional summary
    - Experience: job titles, companies, dates, responsibilities, achievements
    - Education: institutions, degrees, fields of study, dates
    - Certifications
    - Projects: titles, descriptions, technologies, dates
    - Skills
    - Languages: language and proficiency levels
    - Achievements
    - Publications: titles, journals, years
    - References: names, contact information, relations

    The resume content:
    {{ resume }}

    If a field is missing, return null for that field.

    Use JSON format:
    {{ ctx.output_format }}
  "#
}
