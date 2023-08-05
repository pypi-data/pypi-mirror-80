from __future__ import absolute_import
from typing import Dict

from aoa.api.base_api import BaseApi


class DatasetTemplateApi(BaseApi):
    path = "/api/datasetTemplates/"

    def find_all(self, projection: str = None, page: int = None, size: int = None, sort: str = None):
        """
        returns all dataset templates of a project

        Parameters:
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): all dataset templates
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection', 'sort', 'page', 'size', 'sort']
        query_vals = [projection, sort, page, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path,
            header_params,
            query_params)

    def find_by_id(self, dataset_template_id: str, projection: str = None):
        """
        returns a dataset of a project

        Parameters:
           dataset_template_id (str): dataset template id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): dataset template
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection']
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + dataset_template_id,
            header_params,
            query_params)

    def find_by_name(self, dataset_template_name: str, projection: str = None):
        """
        returns a dataset template of a project by name

        Parameters:
           dataset_template_name (str): dataset name(string) to find
           projection (str): projection type

        Returns:
            (dict): dataset template
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['name', 'projection']
        query_vals = [dataset_template_name, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + "search/findByName",
            header_params,
            query_params)

    def save(self, dataset_template: Dict[str, str]):
        """
        register a dataset template

        Parameters:
           dataset template (dict): dataset template to register

        Returns:
            (dict): dataset template
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list',
                'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        self.required_params(['name', 'templateBody', 'parameters'], dataset_template)

        query_params = {}

        return self.aoa_client.post_request(
            self.path,
            header_params,
            query_params,
            dataset_template)

    def apply_template(self, template_request: Dict[str, str]):
        """
        render a dataset template with parameter values

        Parameters:
           template_request (dict): request containing the 'datasetTemplateId'(uuid)
           and 'parameterOverrides'(dict) with the values to render the template

        Returns:
            (dict): rendered dataset template
        """
        header_vars = ['AOA-Project-ID', 'Content-Type', 'Accept']
        header_vals = [
        self.aoa_client.project_id,
        'application/json',
        self.aoa_client.select_header_accept([
            'application/json',
            'application/hal+json',
            'text/uri-list',
            'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        self.required_params(['datasetTemplateId', 'parameterOverrides'], template_request)

        query_params = {}

        return self.aoa_client.post_request(
            self.path + "applyTemplate",
            header_params,
            query_params,
            template_request)
