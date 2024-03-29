import pytest

from unittest.mock import Mock, MagicMock

from ..api.websitesAPI import WebsitesAPI
from ..api.internalAPI import InternalAPI

from ..scraper.Provider import Provider
from ..scraper.Scraper import Scraper
from ..scraper.Task import Task

from .. import scraper

task = Task(10, 50, 45, 5)

rent_canada = Provider("rentCanada")
rent_faster = Provider("rentFaster")
rent_seeker = Provider("rentSeeker")

websites_api = Mock()
websites_api.scrape_rent_canada = MagicMock(return_value="temp")
websites_api.scrape_rent_faster = MagicMock(return_value="temp")
websites_api.scrape_rent_seeker = MagicMock(return_value="temp")

internal_api = Mock()
internal_api.ask_for_tasks = MagicMock(return_value="temp")
internal_api.report_findings = MagicMock(return_value="temp")
internal_api.mark_task_complete = MagicMock(return_value="temp")


def provider_canada():
    p = Provider("rentCanada")
    return p


def test_p_canada():
    assert provider_canada().type == "rentCanada"


def arrange_rent_canada():
    scraper = Scraper(rent_canada, internal_api, websites_api)
    return scraper.scrape(task)


def arrange_rent_faster():
    scraper = Scraper(rent_faster, internal_api, websites_api)
    return scraper.scrape(task)


def arrange_rent_seeker():
    scraper = Scraper(rent_seeker, internal_api, websites_api)
    return scraper.scrape(task)


def test_rent_canada():
    results = arrange_rent_canada()
    expected_query_string = "https://www.rentcanada.com/api/map-markers?filters=%7B%22amenities%22:%7B%22checklist%22:[]%7D,%22utilities%22:%7B%22checklist%22:[]%7D,%22petPolicies%22:%7B%22checklist%22:[]%7D,%22rentalTypes%22:%7B%22checklist%22:[]%7D,%22beds%22:%7B%22min%22:null,%22max%22:null,%22checklist%22:[]%7D,%22baths%22:%7B%22min%22:null,%22max%22:null,%22checklist%22:[]%7D,%22rates%22:%7B%22min%22:null,%22max%22:null%7D,%22sqft%22:%7B%22min%22:null,%22max%22:null%7D,%22mapBounds%22:%7B%22north%22:%7B%22lat%22:50.05324128737679,%22lng%22:45.042314529418945%7D,%22south%22:%7B%22lat%22:49.94675871262321,%22lng%22:44.957685470581055%7D%7D,%22keyword%22:null,%22furnished%22:null%7D"
    # websites_api.assert_called_with(rent_canada)
    websites_api.scrape_rent_canada.assert_called_with(expected_query_string, None)


def test_rent_faster():
    results = arrange_rent_faster()
    websites_api.scrape_rent_faster.assert_called()


def test_rent_seeker():
    results = arrange_rent_seeker()
    websites_api.scrape_rent_seeker.assert_called()
