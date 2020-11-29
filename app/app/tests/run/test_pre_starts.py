# import pytest
#
# from app.tests_pre_start import main
#
# #
# # def test_init():
# #     try:
# #         init()
# #     except Exception as e:
# #         pytest.fail(e)
#
#
# def test_main():
#     try:
#         main()
#     except Exception as e:
#         pytest.fail(e)
#
#
# # def test_session_local(mocker):
# #     def mock_execute(self):
# #         return 0
# #
# #     mocker.patch(
# #         # api_call is from slow.py but imported to main.py
# #         'app.db.session.SessionLocal',
# #         SessionLocala
# #     )
# #     assert init() == 1
# #
# #
# #     # mocker.patch(
# #     #     # api_call is from slow.py but imported to main.py
# #     #     'app.tests_pre_start.SessionLocal',
# #     #     return_value=1
# #     # )
# #
# #
# #
# #     # mocker.patch('app.tests_pre_start.SessionLocal', return_value=SessionLocal())
# #
# #     # assert init() == 1
# #
# #     # try:
# #     #     # Try to create session to check if DB is awake
# #     #     db = SessionLocal()
# #     #     db.execute("SELECT 1")
# #     # except Exception as e:
# #     #     logger.error(e)
# #     #     raise e
# #
#
# # # @patch.object(SessionLocal(), 'execute')
# # # def test_asd(self, DBSession):
# # #     DBSession.execute.query.execute.all.return_value = [1, 2, 3]
# # # @patch('app.tests_pre_start.SessionLocal')
# # @patch('app.tests_pre_start.SessionLocal.execute')
# # def test_init_without_db_connection(test_patch):
# #
# #     # class MockedSessionLocal:
# #     #     def execute(self):
# #     #         return Exception
# #
# #     test_patch.return_value = 123
# #
# #     try:
# #         init()
# #     except Exception as e:
# #         pytest.fail(e)
# #
# #     # SessionLocal.execute = Exception
# #     # mocker.patch(
# #     #     # api_call is from slow.py but imported to main.py
# #     #     'app.tests_pre_start.SessionLocal.execute',
# #     #     return_value=5
# #     # )
# #
# #     # mocker.patch.object(app.tests_pre_start, 'SessionLocal', 2)
# #
# #     # mocker.patch('SessionLocal.execute', return_value=Exception)
# #     # SessionLocal().execute(3)
# #     # mock_method.assert_called_with("SELECT 1;")
# #     #
# #     # mocker =
# #     #
# #     # try:
# #     #     init()
# #     # except Exception as e:
# #     #     pytest.fail(e)
