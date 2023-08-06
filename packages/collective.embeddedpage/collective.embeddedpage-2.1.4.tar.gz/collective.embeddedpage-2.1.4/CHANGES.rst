Changelog
=========


2.1.4 (2020-09-26)
------------------

- Do not fail on invalid URLs
  [timo]

- Run black on codebase
  [timo]


2.1.3 (2020-06-27)
------------------

- Don't purge behaviors
  [csenger]


2.1.2 (2020-06-18)
------------------

- Fix getting js resources (#28).
  [csenger]


2.1.1 (2020-05-06)
------------------

- Do not fail on missing params in process_page.
  [timo]


2.1.0 (2020-05-04)
------------------

- Added i18n translation files for EN, ES, CA.
  [robdayz]

- Add serializer for Volto support.
  [rodfersou]


2.0.0 (2020-04-09)
------------------

- Plone 5.2/Python 3 compatibility.
  [timo,rodfersou]


1.3.2 (2020-02-04)
------------------

- Don't raise an exception when target page is empty.
  [rodfersou]


1.3.1 (2019-06-12)
------------------

- Change development status to Production/Stabel in setup.py.
  [timo]


1.3.0 (2019-06-12)
------------------

- Change header forwarding: Only forward http x-* headers and convert
  zopes header names (e.g. HTTP_X_FORWARD_FOR to x-forward-for)
  [csenger]


1.2.2 (2019-05-28)
------------------

- Dont double decode XML HTML pages.
  [rofersou]

- Pass headers forward from original request.
  [rodfersou]

- Make URL field not required.
  [rodfersou]


1.2.1 (2019-05-10)
------------------

- Fix German translation "Show After" and "Show Before".
  [timo]


1.2.0 (2019-05-10)
------------------

- Use chardet package to detect the encoding of the embedded page.
  [rodfersou]


1.1.0 (2019-04-18)
------------------

- Move stylesheets from head to body.
  [rodfersou]

- Add tests.
  [rodfersou]

- Add data-embedded attribute to inspect what page
  is being embedded with no need to login.
  [rodfersou]


1.0.2 (2019-03-30)
------------------

- Fix the content type when request script.
  [rodfersou]

- Fix iframe relative path to full path.
  [rodfersou]


1.0.1 (2019-03-28)
------------------

- Forward script requests from plone server.
  [rodfersou]

- Forward requests and params to original page.
  [rodfersou]

- Convert html parsed data to string with html method.
  [rodfersou]


1.0.0 (2019-02-23)
------------------

- Re-release 1.0.0a6 as final release.
  [timo]


1.0.0a6 (2019-02-13)
--------------------

- Add extra standard behaviors.
  [rodfersou]


1.0.0a5 (2019-02-12)
--------------------

- Fix when html is encoded as UTF-8.
  [rodfersou]


1.0.0a4 (2019-02-11)
--------------------

- Fix when there is no body tag inside html.
  [rodfersou]


1.0.0a3 (2019-01-22)
--------------------

- Add Rich Text to add content before the page embedded.
  [rodfersou]

- Add Rich Text to add content after the page embedded.
  [rodfersou]

- Add One parameter to disable right portlet column.
  [rodfersou]


1.0.0a2 (2019-01-14)
--------------------

- Do not show title and description of the content page itself.
  [timo]

- Add pypi classifier for development status.
  [timo]


1.0.0a1 (2018-11-01)
--------------------

- Initial release.
  [kitconcept]
