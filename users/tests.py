from django.test import TestCase
from .models import Grad, Opština, Ulaz, CustomUser, Upravnik

# Create your tests here.


class UsersTestCase(TestCase):
    def setUp(self):
        self.user_password = "azerty123"
        self.grad = Grad.objects.create(name="Beograd")
        self.opstina = Opština.objects.create(name="Novi Beograd", Grad=self.grad)
        self.ulaz = Ulaz.objects.create(
            Grad=self.grad,
            Opština=self.opstina,
            Ulica_i_broj="Dusana Vukasovica 74",
        )

    def test_create_user(self):
        self.assertEqual(CustomUser.objects.count(), 0)
        CustomUser.objects.create_user(
            username="damir",
            password=self.user_password,
            Grad=self.grad,
            Opština=self.opstina,
            Ulica_i_broj="Dusana Vukasovica 74",
        )
        

    def test_create_superuser(self):
        pass

    def test_create_upravnik(self):
        pass
