#!/usr/bin/env python
"""
Unit, codeStyle, and end2end tests. To launch, use command:
python3 -m unittest utest_windriver-api.py

Personally I prefer vaRiable style of variables. But to get good scores in the pylint,
I used, in another files, more standard way like va_riable. It depends of team code style.
I can use each. Because I don't test this file with pylint (but we definatly can do
this sort of recursion!) I use here the first style
"""

import unittest
import os
import requests
import api.string_processing

"""
If you launch unittests outside kubernetes/helm chart, please comment next 3 vars 
and uncomment 3 other 
"""
serviceName = os.environ.get("serviceName")
servicePort = os.environ.get("servicePort")
minimum_score = os.environ.get("minimumScore")
#minimum_score = 9.0
# serviceName = restapi-svc-windriver
# servicePort = 9090

headers2Post = {"Content-Type": "application/json"}
url2Start = "http://" + serviceName + ":" + str(servicePort) + "/api/"


class unitTests(unittest.TestCase):
    """
    Unit tests for encrypt/decrypt endpoints and for health enpoint too
    """

    def test_encrypt_ok(self):
        """
        Let's check encrypt function using sample data!
        """
        output = api.string_processing.encrypt_str({"Input": "c3RyaW5n"})
        self.assertTrue(type(output[0]) is dict, msg="Strange output!")
        self.assertEqual(output[1], 200, msg="status code is wrong!")
        self.assertEqual(output[0]["Output"], "YzNSeWFXNW4=", "output is wrong!")
        self.assertEqual(output[0]["Message"], "", "error message is not empty!")
        self.assertEqual(output[0]["Status"], "success", "status is not success!")
        self.assertEqual(
            output[0]["Input"],
            "c3RyaW5n",
            "input in the result should be same as in the PUT request",
        )

    def test_decrypt_ok(self):
        """
        Let's check decrypt function using sample data!
        """
        output = api.string_processing.decrypt_str({"Input": "YzNSeWFXNW4="})
        self.assertTrue(type(output[0]) is dict, msg="Strange output!")
        self.assertEqual(output[1], 200, msg="status code is wrong!")
        self.assertEqual(output[0]["Output"], "c3RyaW5n", "output is wrong!")
        self.assertEqual(output[0]["Message"], "", "error message is not empty!")
        self.assertEqual(output[0]["Status"], "success", "status is not success!")
        self.assertEqual(
            output[0]["Input"],
            "YzNSeWFXNW4=",
            "input in the result should be same as in the PUT request",
        )

    def test_health(self):
        """
        Checking health endpoint for kubernetes
        """
        welcome_output = api.string_processing.welcome_endpoint()
        self.assertEqual(welcome_output[0], "", msg="Output should be empty string!")
        self.assertEqual(welcome_output[1], 204, msg="HTTP code should be 204")

    def test_FailDecryptTest(self):
        """
        This is unittest, which should fail
        """
        output = api.string_processing.decrypt_str({"Input": "c3RasdW5n="})
        self.assertEqual(output[1], 415, msg="status code is wrong!")
        # Should be not empty. Than bool('...') -> True
        self.assertTrue(
            bool(output[0]["Message"]), f"Message is empty in the failed request!"
        )
        self.assertEqual(output[0]["Status"], "error", 'Status should be "error"!')
        # should be empty. Than not bool('') -> True
        self.assertTrue(
            not bool(output[0]["Output"]),
            f"Message is not empty in the failed request!",
        )

    def test_FailEncryptTest(self):
        """
        This is unittest, which should fail
        """
        output = api.string_processing.encrypt_str({"Input": "¥"})
        self.assertEqual(output[1], 415, msg="status code is wrong!")
        # Should be not empty. Than bool('...') -> True
        self.assertTrue(
            bool(output[0]["Message"]), f"Message is empty in the failed request!"
        )
        self.assertEqual(output[0]["Status"], "error", 'Status should be "error"!')
        # should be empty. Than not bool('') -> True
        self.assertTrue(
            not bool(output[0]["Output"]),
            f"Message is not empty in the failed request!",
        )


class strictTypingTests(unittest.TestCase):
    """
    Here we check types in functions of our API. Overall, they're already checked by
    Swagger using swagger yaml file. Here we have have one unittest, and one syntax analizator test
    """

    def test_generate_output(self):
        """
        Everything should be string!
        """
        str_e = "string_example"
        typing_status = True
        try:
            api.string_processing.generate_output(str_e, str_e, str_e, str_e)
        except KeyError:
            typing_status = False
        self.assertTrue(
            typing_status,
            msg="strict typing implementation helped us to catch type mismatch error!",
        )

    def test_strictTypesDoubleCheck(self):
        """
        mypy is cli tool to check python strict types if they uses in the code
        shell exit code 0 is True. But for python it's False. We have to revert bool
        """
        self.assertTrue(not os.system("mypy api/string_processing.py"))


class codeStyleTests(unittest.TestCase):
    """
    Set of code style/pylint tests
    """
    def test_pylintStatus_entry_point(self):
        """
        Check code style via pylint
        exit code 0 is True. But for python it's False. We have to revert bool
        """
        self.assertTrue(
            not os.system(f"pylint --fail-under={minimum_score} windriver_api.py")
        )

    def test_pyLintStatus_string_processing(self):
        """
        Check code style via pylint
        exit code 0 is True. But for python it's False. We have to revert bool
        """
        self.assertTrue(
            not os.system(
                f"pylint --fail-under={minimum_score}  api/string_processing.py"
            )
        )


class end2EndTests(unittest.TestCase):
    """
    end2end tets which should check the real HTTP endpoints
    """

    def test_end2EndEncrypt(self):
        """
        check encryption - check it's status code
        """
        url2Parse = url2Start + "encrypt"
        payLoad = '{"Input": "string"}'
        r = requests.post(url=url2Parse, data=payLoad, headers=headers2Post)
        self.assertEqual(r.status_code, 200)

    def test_end2EndDecrypt(self):
        """
        check decryption
        """
        url2Parse = url2Start + "decrypt"
        payLoad = '{"Input": "c3RyaW5n"}'
        r = requests.post(url=url2Parse, data=payLoad, headers=headers2Post)
        self.assertEqual(r.status_code, 200)

    def test_health(self):
        """
        Post request for /health endpoint
        """
        url2Parse = url2Start + "health"
        r = requests.get(url=url2Parse, headers=headers2Post)
        self.assertEqual(r.status_code, 204)

    def test_end2FailDecryptTest(self):
        """
        Fail end2end test #1
        """
        url2Parse = url2Start + "decrypt"
        # incorrect base64 hash
        payLoad = '{"Input": "c3RasdW5n"}'
        r = requests.post(url=url2Parse, data=payLoad, headers=headers2Post)
        self.assertEqual(r.status_code, 415)

    def test_end2FailEncryptTest(self):
        """
        Fail end2end test #2
        """
        url2Parse = url2Start + "encrypt"
        # non-ASCII
        payLoad = '{"Input": "¥"}'
        r = requests.post(url=url2Parse, data=payLoad, headers=headers2Post)
        # assertation error
        self.assertEqual(r.status_code, 400)


if __name__ == "__main__":
    unittest.main()
