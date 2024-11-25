from datetime import date

from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.urls import reverse

from dictionaries.admin import (
    ScheduleTemplateAdmin,
    ScheduleAdmin,
    StudentMarkAdmin
)
from dictionaries.models import (
    StudyGroup,
    Term,
    Subject,
    ScheduleTemplate,
    Schedule,
    StudentMark
)


class TestAdminSite(AdminSite):
    pass


admin_site = TestAdminSite()


class AdminTests(TestCase):
    """
    Test all admin functionalities such as creating, editing, and deleting
    records.
    """

    def setUp(self):
        """
        Setup test environment. Create a superuser and required model
        instances.
        """
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password'
        )
        self.active_user = User.objects.create_user(
            username="active_user",
            is_active=True
        )
        self.inactive_user = User.objects.create_user(
            username="inactive_user",
            is_active=False
        )

        self.study_group = StudyGroup.objects.create(
            name="Group A",
            active=True
        )
        self.term = Term.objects.create(
            name="2024-2025 Term 1",
            date_from=date(2024, 1, 1),
            date_to=date(2024, 5, 31),
            active=True
        )
        self.subject = Subject.objects.create(name="subject1", active=True)
        self.schedule_template = ScheduleTemplate.objects.create(
            term=self.term,
            study_group=self.study_group,
            weekday=1,
            order_number=1,
            subject=self.subject
        )
        self.schedule = Schedule.objects.create(
            study_group=self.study_group,
            date="2024-04-01",
            order_number=1,
            subject=self.subject,
            homework="Do homework"
        )
        self.student_mark = StudentMark.objects.create(
            schedule=self.schedule,
            student=self.superuser,
            mark=90
        )

        self.inactive_term = Term.objects.create(
            name="2024-2025 Term 2",
            date_from="2024-07-01",
            date_to="2024-12-31",
            active=False
        )
        self.inactive_study_group = StudyGroup.objects.create(
            name="Group B",
            active=False
        )
        self.inactive_subject = Subject.objects.create(
            name="subject2",
            active=False
        )

        self.schedule_template_admin = ScheduleTemplateAdmin(
            ScheduleTemplate,
            admin_site
        )
        self.schedule_admin = ScheduleAdmin(Schedule, admin_site)
        self.student_mark_admin = StudentMarkAdmin(StudentMark, admin_site)

        self.client = Client()
        self.client.login(username='admin', password='password')

    def test_admin_list_view(self):
        """
        Test the admin list view for StudyGroup, Term, Subject,
        ScheduleTemplate, and Schedule.
        """
        # Create an admin user and log in
        self.client.login(username='admin', password='password')

        url = reverse('admin:dictionaries_scheduletemplate_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('admin:dictionaries_studygroup_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('admin:dictionaries_term_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('admin:dictionaries_subject_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        url = reverse('admin:dictionaries_schedule_changelist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_admin_search_fields(self):
        """
        Test that the admin search functionality for StudyGroup works as
        expected.
        """
        url = reverse('admin:dictionaries_studygroup_changelist') + "?q=Group"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Group A")

    def test_admin_filter_functionality(self):
        """ Test that the admin filter functionality works correctly. """
        url = (
            reverse('admin:dictionaries_scheduletemplate_changelist') +
            "?study_group=" + str(self.study_group.id)
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2024-2025 Term 1")

        url_with_term = (
            reverse('admin:dictionaries_scheduletemplate_changelist') +
            "?term=" + str(self.term.id)
        )
        response_with_term = self.client.get(url_with_term)

        self.assertEqual(response_with_term.status_code, 200)
        self.assertContains(response_with_term, "Group A")

    def test_admin_create_update_delete(self):
        """ Test the creation, updating, and deletion of admin objects. """
        # The admin user logs in
        self.client.login(username='admin', password='password')

        # Create a StudyGroup object via the admin panel
        create_url = reverse('admin:dictionaries_studygroup_add')
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)

        # Submit form to create StudyGroup object
        data = {'name': 'Test Group', 'active': True}
        response = self.client.post(create_url, data)
        self.assertRedirects(
            response,
            reverse('admin:dictionaries_studygroup_changelist')
        )

        # Update the created object
        study_group = StudyGroup.objects.get(name='Test Group')
        update_url = reverse(
            'admin:dictionaries_studygroup_change',
            args=[study_group.pk]
        )
        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)

        # Submit form to update StudyGroup object
        updated_data = {'name': 'Updated Group', 'active': False}
        response = self.client.post(update_url, updated_data)
        self.assertRedirects(
            response,
            reverse('admin:dictionaries_studygroup_changelist')
        )

        # Delete the created object
        delete_url = reverse(
            'admin:dictionaries_studygroup_delete',
            args=[study_group.pk]
        )
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)

        # Confirm the deletion
        response = self.client.post(delete_url, {'post': 'yes'})
        self.assertRedirects(
            response,
            reverse('admin:dictionaries_studygroup_changelist')
        )

    def test_admin_permissions(self):
        """ Test that only admins have access to the admin panel. """
        non_admin_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='password'
        )
        # Try to login as non-admin user and access the admin panel
        self.client.login(username='user', password='password')
        url = reverse('admin:dictionaries_studygroup_changelist')
        response = self.client.get(url)

        self.assertRedirects(response, '/admin/login/?next=' + url)

        # Logout the non-admin user
        self.client.logout()

        # Now login as admin user and check access to the admin panel
        self.client.login(username='admin', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_term_foreignkey_queryset(self):
        """
        Test that the queryset for the 'term' foreign key is correctly filtered
        to include only active terms. The test ensures that inactive terms are
        excluded from the queryset.
        """
        field = ScheduleTemplate._meta.get_field('term')
        formfield = self.schedule_template_admin.formfield_for_foreignkey(
            field,
            None
        )
        terms = formfield.queryset
        # Ensure only active terms are included
        self.assertIn(self.term, terms)
        self.assertNotIn(self.inactive_term, terms)

    def test_study_group_foreignkey_queryset(self):
        """
        Test that the queryset for the 'study_group' foreign key is correctly
        filtered to include only active study groups. The test ensures that
        inactive study groups are excluded from the queryset.
        """
        field = ScheduleTemplate._meta.get_field('study_group')
        formfield = self.schedule_template_admin.formfield_for_foreignkey(
            field,
            None
        )
        study_groups = formfield.queryset
        # Ensure only active study groups are included
        self.assertIn(self.study_group, study_groups)
        self.assertNotIn(self.inactive_study_group, study_groups)

    def test_subject_foreignkey_queryset(self):
        """
        Test that the queryset for the 'subject' foreign key is correctly
        filtered to include only active subjects.
        The test ensures that inactive subjects are excluded from the queryset.
        """
        field = ScheduleTemplate._meta.get_field('subject')
        formfield = self.schedule_template_admin.formfield_for_foreignkey(
            field,
            None
        )
        subjects = formfield.queryset
        # Ensure only active subjects are included
        self.assertIn(self.subject, subjects)
        self.assertNotIn(self.inactive_subject, subjects)

    def test_study_group_foreign_key_filter(self):
        """
        Test that the queryset for the 'study_group' foreign key includes only
        active study groups.
        """
        field = Schedule._meta.get_field('study_group')
        formfield = self.schedule_admin.formfield_for_foreignkey(field, None)

        study_groups = formfield.queryset

        self.assertIn(self.study_group, study_groups)
        self.assertNotIn(self.inactive_study_group, study_groups)

    def test_subject_foreign_key_filter(self):
        """
        Test that the queryset for the 'subject' foreign key includes only
        active subjects.
        """
        field = Schedule._meta.get_field('subject')
        formfield = self.schedule_admin.formfield_for_foreignkey(field, None)

        subjects = formfield.queryset

        self.assertIn(self.subject, subjects)
        self.assertNotIn(self.inactive_subject, subjects)

    def test_student_foreign_key_filter(self):
        """
        Test that the queryset for the 'student' foreign key includes only
        active users.
        """
        field = StudentMark._meta.get_field('student')
        formfield = self.student_mark_admin.formfield_for_foreignkey(
            field,
            None
        )

        students = formfield.queryset

        self.assertIn(self.active_user, students)
        self.assertNotIn(self.inactive_user, students)
