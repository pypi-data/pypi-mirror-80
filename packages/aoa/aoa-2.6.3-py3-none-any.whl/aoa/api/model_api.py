from __future__ import absolute_import
from typing import Dict

from aoa.api.base_api import BaseApi


class ModelApi(BaseApi):

    path = "/api/models/"

    def find_all(self, projection: str = None):
        """
        returns all models

        Parameters:
           projection (str): projection type

        Returns:
            (dict): all models
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
            self.path,
            header_params,
            query_params)

    def find_by_id(self, model_id: str, projection: str = None):
        """
        returns a model

        Parameters:
           model_id (str): model id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): model
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
            self.path + model_id,
            header_params,
            query_params)

    def find_all_commits(self, model_id: str, projection: str = None):
        """
        returns model commits

        Parameters:
           model_id (str): model id(uuid) for commits
           projection (str): projection type

        Returns:
            (dict): model commits
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
            self.path + model_id + '/commits',
            header_params,
            query_params)

    def diff_commits(self, model_id: str, commit_id1: str, commit_id2: str, projection: str = None):
        """
        returns difference between model commits

        Parameters:
           model_id (str): model id(uuid)
           commit_id1 (str): id of commit to compare
           commit_id2 (str): id of commit to compare
           projection (str): projection type

        Returns:
            (str): difference between model commits
        """
        header_vars = ['AOA-Project-ID', 'Accept']
        header_vals = [
            self.aoa_client.project_id,
            self.aoa_client.select_header_accept([
                'application/json',
                'application/hal+json',
                'text/uri-list', 'application/x-spring-data-compact+json'])]
        header_params = self.generate_params(header_vars, header_vals)

        query_vars = ['projection']
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.aoa_client.get_request(
            self.path + model_id +
            '/diff/' + commit_id1 + '/' + commit_id2 + '/',
            header_params,
            query_params)

    def save(self, model: Dict[str, str]):
        """
        register a dataset

        Parameters:
           model (dict): external model to register

        Returns:
            (dict): model
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

        self.required_params(['name', 'description', 'externalModelAttributes'], model)

        query_params = {}

        return self.aoa_client.post_request(
            self.path,
            header_params,
            query_params,
            model)
