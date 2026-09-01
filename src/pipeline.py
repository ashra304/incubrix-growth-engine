from src.creator_discovery import discover_creators
from src.lead_builder import build_lead
from src.qualification import qualify_creator
from src.deduplication import deduplicate_leads
from src.priority import calculate_priority
from src.personalization import generate_personalization_hook
from src.completeness import check_completeness
from src.duplicate_check import check_duplicate
from src.exporter import export_leads_to_csv
from src.freshness import is_evidence_within_30_days

def run_pipeline(
    query: str,
    max_results: int = 10,
):
    """
    Run the complete creator discovery pipeline.

    Flow:

        YouTube Discovery
            ↓
        Activity Verification
            ↓
        Evidence Collection
            ↓
        Lead Construction
            ↓
        Qualification
          ↙       ↘
    Qualified    Rejected
        ↓
      Priority
        ↓
    Personalization
        ↓
    Completeness
        ↓
    Duplicate Check
        ↓
    Deduplication
        ↓
    CSV Export
        ↓
    Final Qualified Leads
    """

    # ---------------------------------------------------------
    # 1. DISCOVER + COLLECT EVIDENCE
    # ---------------------------------------------------------

    discovered = discover_creators(
        query=query,
        max_results=max_results,
    )

    all_leads = []
    rejected_leads = []

    # ---------------------------------------------------------
    # 2. PROCESS EACH CREATOR
    # ---------------------------------------------------------

    for candidate, activity, evidence in discovered:

        # -----------------------------------------------------
        # 3. BUILD LEAD
        # -----------------------------------------------------

        lead = build_lead(
            candidate=candidate,
            activity=activity,
            evidence=evidence,
            lead_id=f"YT-{candidate.stable_creator_id}",
        )

        # -----------------------------------------------------
        # 4. PREPARE QUALIFICATION SIGNALS
        # -----------------------------------------------------

        active_30d = (
            (activity.get("content_count_30d") or 0) > 0
        )

        long_form_60d = (
            (activity.get("longform_count_60d") or 0) > 0
        )

        contactable = bool(
            evidence.business_contact
        )

        complete_fields = all(
            [
                bool(lead.creator_name),
                bool(lead.creator_segment),
                bool(lead.country_iso2),
                bool(lead.primary_language),
                bool(lead.primary_platform),
                bool(lead.profile_url),
                bool(lead.stable_creator_id),
            ]
        )

        # -----------------------------------------------------
        # 5. QUALIFICATION
        # -----------------------------------------------------

        qualification = qualify_creator(
            creator_segment=lead.creator_segment,
            country_iso2=lead.country_iso2,
            primary_language=lead.primary_language,
            has_official_profile=bool(lead.profile_url),
            has_stable_creator_id=bool(lead.stable_creator_id),
            active_30d=active_30d,
            long_form_60d=long_form_60d,
            commercial_signal=evidence.commercial_signal,
            incubrix_need=evidence.incubrix_need,
            contactable=contactable,
            complete_fields=complete_fields,
            unique_creator=True,
            evidence_within_30d=is_evidence_within_30_days(
                lead.checked_date
            ),
        )

        # -----------------------------------------------------
        # 6. STORE QUALIFICATION RESULT
        # -----------------------------------------------------

        if qualification.qualified:

            lead.candidate_status = "qualified"

        else:

            lead.candidate_status = "rejected"

            lead.rejection_reason = "; ".join(
                qualification.rejection_reasons
            )

            rejected_leads.append(lead)

            continue

        # -----------------------------------------------------
        # 7. CALCULATE PRIORITY
        # -----------------------------------------------------

        priority_result = calculate_priority(
            qualified=qualification.qualified,
            commercial_signal=evidence.commercial_signal,
            incubrix_need=evidence.incubrix_need,
            contactable=contactable,
            active_30d=active_30d,
            long_form_60d=long_form_60d,
        )

        lead.priority = priority_result.priority

        # -----------------------------------------------------
        # 8. GENERATE PERSONALIZATION HOOK
        # -----------------------------------------------------

        lead.personalization_hook = (
            generate_personalization_hook(
                creator_name=lead.creator_name,
                creator_segment=lead.creator_segment,
                commercial_signal=evidence.commercial_signal,
                incubrix_need=evidence.incubrix_need,
                active_30d=active_30d,
                long_form_60d=long_form_60d,
            )
        )

        # -----------------------------------------------------
        # 9. CHECK LEAD COMPLETENESS
        # -----------------------------------------------------

        completeness_result = check_completeness(
            lead
        )

        if completeness_result.complete:

            lead.completeness_check = "complete"

        else:

            lead.completeness_check = (
                "missing: "
                + ", ".join(
                    completeness_result.missing_fields
                )
            )

        # -----------------------------------------------------
        # 10. CHECK DUPLICATE
        # -----------------------------------------------------

        duplicate_result = check_duplicate(
            lead,
            all_leads,
        )

        if duplicate_result.is_duplicate:

            lead.duplicate_check = (
                "duplicate: "
                + duplicate_result.reason
            )

        else:

            lead.duplicate_check = "unique"

        # -----------------------------------------------------
        # 11. STORE QUALIFIED LEAD
        # -----------------------------------------------------

        all_leads.append(lead)

    # ---------------------------------------------------------
    # 12. DEDUPLICATE
    # ---------------------------------------------------------

    final_leads = deduplicate_leads(
        all_leads
    )

    # ---------------------------------------------------------
    # 13. EXPORT FINAL QUALIFIED LEADS
    # ---------------------------------------------------------

    export_path = export_leads_to_csv(
        final_leads,
        "data/final_leads.csv",
    )

    # ---------------------------------------------------------
    # 14. PIPELINE SUMMARY
    # ---------------------------------------------------------

    print(
        f"TOTAL DISCOVERED: {len(discovered)}"
    )

    print(
        f"QUALIFIED: {len(all_leads)}"
    )

    print(
        f"REJECTED: {len(rejected_leads)}"
    )

    print(
        f"FINAL LEADS: {len(final_leads)}"
    )

    print(
        f"EXPORT: {export_path}"
    )

    return final_leads


if __name__ == "__main__":

    results = run_pipeline(
        query="technology creators",
        max_results=5,
    )

    for lead in results:

        print(
            "\n"
            f"Creator: {lead.creator_name}\n"
            f"Country: {lead.country_iso2}\n"
            f"Language: {lead.primary_language}\n"
            f"Contact: {lead.business_contact}\n"
            f"Commercial: {lead.monetization_signal}\n"
            f"IncuBrix Need: {lead.incubrix_need}\n"
            f"Priority: {lead.priority}\n"
            f"Personalization: {lead.personalization_hook}\n"
            f"Completeness: {lead.completeness_check}\n"
            f"Duplicate Check: {lead.duplicate_check}\n"
            f"Status: {lead.candidate_status}\n"
        )