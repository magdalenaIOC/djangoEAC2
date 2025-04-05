from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MySeleniumTests(StaticLiveServerTestCase):
    #carregar una BD de test
    fixtures = ['testdb.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        # creem superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()


    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        cls.selenium.quit()
        super().tearDownClass()

    def login_com_superusuari(self):
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )

        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        # testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
        self.assertEqual( self.selenium.title , "Site administration | Django site admin" )


    def test_login(self):
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )

        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        # testejem que hem entrat a l'admin panel comprovant el títol de la pàgina
        self.assertEqual( self.selenium.title , "Site administration | Django site admin" )


    def test_creacio_usuari(self):
        # entrem com a superusuari
        self.login_com_superusuari()

        # Clicar "Users"
        self.selenium.find_element(By.LINK_TEXT, "Users").click()

        # Clicar "Add user"
        self.selenium.find_element(By.LINK_TEXT, "ADD USER").click()

        # Introduir usuari i contrasenya
        self.selenium.find_element(By.NAME, "username").send_keys("magdalena")
        self.selenium.find_element(By.NAME, "password1").send_keys("P4ssw0rd321")
        self.selenium.find_element(By.NAME, "password2").send_keys("P4ssw0rd321")

        # Desar i continuarPassar a la següent pàgina
        self.selenium.find_element(By.NAME, "_continue").click()

        # Marcar "staff"
        self.selenium.find_element(By.ID, "id_is_staff").click()

        # Desar l’usuari
        self.selenium.find_element(By.NAME, "_save").click()

        # Verificar que l'usuari s’ha creat amb èxit

        self.assertIn("successfully", self.selenium.find_element(By.CLASS_NAME, "success").text)

    def test_existeix_login(self):
        # entrem com a superusuari
        self.login_com_superusuari()

        # Verificam si ens surt el Login després que l'usuari s'hagi identificat correctament
        try:
            #self.selenium.find_element(By.XPATH,'//input[@value="Log in"]')
            self.selenium.find_element(By.XPATH,'//button[text(),"Logout"]')
            assert False, "Trobat element LOGIN que no hi ha de ser"
        except NoSuchElementException:
            pass
