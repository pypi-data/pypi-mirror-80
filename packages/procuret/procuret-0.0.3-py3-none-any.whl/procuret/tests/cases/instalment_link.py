"""
Procuret Python
Exercise Instalment Link Test
author: hugh@blinkybeach.com
"""
from procuret.tests.variants.with_supplier import TestWithSupplier
from procuret.tests.test_result import Success, TestResult
from procuret.instalment_link import InstalmentLink
from procuret.session import Session, Perspective
from procuret.ancillary.communication_option import CommunicationOption
from decimal import Decimal


class ExerciseInstalmentLink(TestWithSupplier):

    NAME = 'Create an InstalmentLink'

    def execute(self) -> TestResult:

        session = Session.create_with_email(
            email=self.email,
            plaintext_secret=self.secret,
            perspective=Perspective.SUPPLIER
        )

        link = InstalmentLink.create(
            supplier=self.supplier_id,
            invoice_amount=Decimal('422.42'),
            invitee_email='noone@procuret-test-domain.org',
            invoice_identifier='Test 42',
            communication=CommunicationOption.EMAIL_CUSTOMER,
            session=session
        )

        assert isinstance(link, InstalmentLink)

        return Success()
