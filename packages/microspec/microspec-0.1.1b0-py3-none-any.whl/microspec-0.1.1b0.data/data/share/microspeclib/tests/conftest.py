import pytest

# Copyright 2020 by Chromation, Inc
# All Rights Reserved by Chromation, Inc

@pytest.fixture(scope="class")
def class_results(request):
  request.cls.results = [["Command", "Time(ms)"]]

