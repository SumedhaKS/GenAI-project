import wikipedia
from pydantic import BaseModel
from typing import List
import re

class InstitutionInfo(BaseModel):
    name: str
    founder: str
    founded_year: str
    branches: List[str]
    num_employees: int
    summary: str

def get_institution_info(name: str) -> InstitutionInfo:
    try:
        # Use search to find the closest page
        search_results = wikipedia.search(name)
        if not search_results:
            raise ValueError(f"No Wikipedia page found for '{name}'")
        
        # Use the top search result
        page_title = search_results[0]
        page = wikipedia.page(page_title)
        content = page.content
        summary = wikipedia.summary(page_title, sentences=4)

        founder = re.search(r"(?i)founder[s]?:? (.+)", content)
        founded = re.search(r"(?i)(established|founded)[^\n\d]*(\d{4})", content)
        branches = re.findall(r"(?i)campus(?:es)? in ([\w, ]+)", content)
        employees = re.search(r"(\d{3,6}) employees", content)

        return InstitutionInfo(
            name=page.title,
            founder=founder.group(1).strip() if founder else "Unknown",
            founded_year=founded.group(2) if founded else "Unknown",
            branches=branches[0].split(",") if branches else [],
            num_employees=int(employees.group(1)) if employees else 0,
            summary=summary
        )

    except wikipedia.exceptions.DisambiguationError as e:
        raise ValueError(f"Ambiguous input. Try one of these: {e.options[:5]}")
    except wikipedia.exceptions.PageError:
        raise ValueError(f"No Wikipedia page found for '{name}'")
    except Exception as e:
        raise RuntimeError(f"An error occurred: {str(e)}")
