import pytest
from playwright.sync_api import Page, expect


def test_matchup_and_reset_user_flow(page: Page):
    """Simulates a user flow through player selection, matchup prompting, observing yields, and resetting."""
    page.context.tracing.start(screenshots=True, snapshots=True)

    page.goto("http://localhost:8000")

    # Select batter
    page_target = page.get_by_label("Batter")
    expect(page_target).to_be_visible()
    page_target.select_option("bo_bichette")

    # Select pitcher
    page_target = page.get_by_label("Pitcher")
    expect(page_target).to_be_visible()
    page_target.select_option("bryan_woo")

    # Invoke matchup
    page_target = page.get_by_role("Button", name="Matchup!")
    expect(page_target).to_be_visible()
    page_target.click()

    page.wait_for_timeout(3000)  # Wait 3 seconds for yields to render

    # See grand score
    page_target = page.locator("#grand-score")
    expect(page_target).not_to_have_text("---")

    # See pitch-type score
    page_target = page.locator("#arsenal-score")
    expect(page_target).not_to_have_text("---")

    # See zone score
    page_target = page.locator("#location-score")
    expect(page_target).not_to_have_text("---")

    # Reset page
    page_target = page.get_by_role("Button", name="Reset")
    expect(page_target).to_be_visible()
    page_target.click()

    page.wait_for_timeout(1000)  # Wait 1 second for page to reset

    # See grand score in null state
    page_target = page.locator("#grand-score")
    expect(page_target).to_have_text("---")

    page.context.tracing.stop(path="trace.zip")
