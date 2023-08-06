"""
   Copyright 2020 Sarus SAS

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   Sarus library to leverage sensitive data without revealing them

   This lib contains classes and method to browse,
   learn from & explore sensitive datasets.
   It connects to a Sarus server, which acts as a gateway, to ensure no
   results/analysis coming out of this lib are sensitive.
"""

import requests
import tempfile
import tarfile
import cloudpickle
import pickle
import tensorflow as tf
import io
import os
import sys
import re
import json
import matplotlib.pyplot as plt
import time
import getpass
import base64


class Dataset:
    """
    A class based on tf.data.dataset to provide a representation of datasets
    used by Sarus, remotely.
    To be shared by client & server.
    """

    def __init__(
        self,
        name,
        id,
        type_metadata=None,
        URI=None,
        human_description=None,
        marginals=None,
        columns=None,
    ):
        self.name = name
        self.id = id
        self.parquet_dataset = None  # TO BE REMOVED ??
        try:
            self.type_metadata = json.loads(type_metadata)
        except Exception:
            self.type_metadata = None
        self.URI = URI
        self.columns = columns
        self.human_description = human_description
        self.synthetic = None
        try:
            self.marginals = json.loads(marginals)
        except Exception:
            self.marginals = None

    def _inputs():
        return None

    def element_spec():
        return None

    def set_real_data(self, parquet_dataset):
        """upload the data into the dataset"""
        self.parquet_dataset = parquet_dataset

    def set_synthetic_data(self, data):
        """upload the data into the dataset"""
        self.synthetic = data

    def set_set_marginals(self, data):
        """upload the data into the dataset"""
        self.marginals = data

    def _plot_marginal_feature(self, marginal_feature, width=1.5, heigth=1.5):
        if "statistics" not in marginal_feature:
            return None

        # text-based representations
        # count for categories
        distrib = marginal_feature["statistics"].get("distribution")
        if distrib:
            html_response = ""
            distrib_s = sorted(distrib, key=lambda x: -x["probability"])
            if len(distrib_s) > 5:
                others_count = len(distrib_s) - 5
                others_sum = sum([x["probability"] for x in distrib_s[5:]])
                distrib_s = distrib_s[0:5]
                distrib_s.append(
                    {
                        "name": f"Other ({others_count})",
                        "probability": others_sum,
                        "class_other": "True",
                    }
                )
            for item in distrib_s:
                html_response += "<div><div class='category "
                if "class_other" in item:
                    html_response += "other"
                html_response += f"''>\
                    {item['name']}\
                  </div>\
                  <div class='number'> {round(100*item['probability'],2)}%\
                  </div>\
                 </div>"
            return html_response

        # Graph-based representation
        _ = plt.figure(figsize=(width, heigth))
        # cumulDistribution for real
        cumul = marginal_feature["statistics"].get("cumulativeDistribution")
        if cumul:
            try:
                plt.fill_between(
                    [vp["value"] for vp in cumul],
                    [vp["probability"] for vp in cumul],
                )
            except Exception:
                pass
        fi = io.BytesIO()
        plt.tight_layout()
        plt.savefig(fi, format="svg")
        plt.clf()
        svg_dta = fi.getvalue()  # this is svg data
        return svg_dta.decode()

    def to_html(self, display_type=False):
        """
        return a HTML representation of this dataset, to be displayed
        in a Notebook for example.
        We'd like to render something like: https://www.kaggle.com/fmejia21/demographics-of-academy-awards-oscars-winners
        """
        css = """<style>
        @import url('https://rsms.me/inter/inter.css');
        @supports (font-variation-settings: normal) {
            html {font-family: 'Inter var', sans-serif; }
            table {font-size: 12px; border-collapse: collapse;}
            td, th {
                border: 1px solid rgb(222, 223, 224);
                font-weight: 500;
                color: rgba(0,0,0,0.7);
                padding: 8px;
                vertical-align:top;
                }
            tr.desc>td>div {
                display: flex; width: 140px;
                flex-wrap: wrap;
                justify-content: space-between;
            }
            tr.desc>td {
                border-bottom-width: 4px;
                }
            div.category {
                width: 70px;
                padding: 4px;
                margin-bottom: 4px;
                color: black;
                }
            div.number {
                padding: 4px;
                margin-bottom: 4px;
                color: rgb(0, 138, 188);
                text-align: right;
            }
            td>div:hover {
                background-color: rgba(0,0,0,0.03);
              }
            tr.synthetic {
                font-family: 'Roboto Mono', Monaco, Consolas, monospace;
              }
            tr.synthetic>td {
                padding: 8px 4px;
                color: rgba(0, 0, 0, 0.7);
              }
            div.other {color: rgba(0, 0, 0, 0.4);!important}
         </style>"""

        table = "<table>\
                <thead><tr>\n"
        columns = self.type_metadata["features"]
        for c in columns:
            table += f"<th>{c['name']}</th>\n"

        table += """</thead></tr>
                <tbody>
                <tr class='desc'>"""

        columns = self.type_metadata["features"]
        for c in self.marginals["features"]:
            table += f"<td>{self._plot_marginal_feature(c)}</td>\n"
        table += "</tr><tr>"
        if display_type:
            for c in columns:
                table += f"<td>{c['type']}</td>\n"

        table += "</tr></tbody></table>"

        return f"<html>{css}<body>\n \
                   {table}\
                 </body></html>"


class Client:
    def _url_validator(self, url):
        """
        From https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
        """
        regex = re.compile(
            r"^(?:http|ftp)s?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )
        return re.match(regex, url) is not None

    def __init__(
        self,
        url="http://0.0.0.0:5000",
        username=None,
        password=None,
        verify=True,
    ):
        # verify: if False, doesn't check SSL certificate if protocol is https
        # TODO : self.progress_bar = Progbar(100, stateful_metrics=None)

        if self._url_validator(url):
            self.base_url = url
        else:
            raise Exception("Bad url")
        self.verify = verify
        if not password:
            password = getpass.getpass(prompt="Password: ", stream=None)
        try:
            request = requests.post(
                f"{self.base_url}/login",
                json={"username": username, "password": password},
                headers={"Content-Type": "application/json"},
                verify=self.verify,
            )
            self.cookies = request.cookies
            request.raise_for_status()
        except Exception:
            raise Exception(
                "Error during login: incorrect username or password"
            )

    def available_datasets(self):
        request = requests.get(
            f"{self.base_url}/datasets",
            cookies=self.cookies,
            verify=self.verify,
        )
        return [ds["name"] for ds in request.json()]

    def fetch_dataset_by_id(self, id):
        """Fetch a dataset from the Sarus Gateway

        Args:
            id (int): id of the dataset to be fetched

        Returns:
            an instance of Dataset
        """
        try:
            request = requests.get(
                f"{self.base_url}/datasets/{id}",
                cookies=self.cookies,
                verify=self.verify,
            )
            dataset = pickle.loads(request.content)
            return dataset
        except Exception:
            raise Exception("Dataset not available")

    def fetch_dataset_by_name(self, name):
        """Fetch a dataset from the Sarus Gateway

        Args:
            name (string): name of the dataset to be fetched

        Returns:
            an instance of Dataset
        """
        try:
            request = requests.get(
                f"{self.base_url}/datasets/name/{name}",
                cookies=self.cookies,
                verify=self.verify,
            )
            dataset = pickle.loads(request.content)
            return dataset
        except Exception:
            raise Exception("Dataset not available")

    def fit(
        self,
        transform_def,
        keras_model_def,
        x=None,
        target_epsilon=None,
        batch_size=64,
        non_DP_training=False,
        dp_l2_norm_clip=1,
        dp_noise_multiplier=1,
        dp_num_microbatches=None,  # default: batch size
        tf_seed=None,
        **kwargs,
    ):
        """
        Launches remotely the training of a model, passed in keras_model_def

        Args:
            transform_def (callable): transform function
            keras_model_def (callable): function returning the model to train
            x (Dataset): dataset used for training
            y (Dataset): (Optional) target dataset used for training
            target_epsilon (float): If set, we stop the training when this value
                is reached
            batch_size (int): batch size
            non_DP_training (bool): if True, we trigger an additional training
                without DP, to compare performances (the resulting model is NOT
                returned)
            dp_l2_norm_clip (float): max value used to clip the gradients during
                DP-SGD training
            dp_noise_multiplier (float): noise multiplier for DP-SGD
            dp_num_microbatches (int): Number of microbatches (by default, equal
                to batch_size, so we get microbatches of size 1)
            tf_seed (int): The tensorflow seed is set to this value before the
                model is trained.
            **kwargs: other kwargs to pass to tensorflow Model.fit() function

        Returns:
            int: Id of the task
        """
        # for retro-compatibility, if y is set, delete it
        if "y" in kwargs:
            del kwargs["y"]

        from tensorflow.keras import Model

        # set the seed
        if tf_seed is not None:
            tf.random.set_seed(tf_seed)

        model: Model = keras_model_def()
        # learn input/output shapes by running predict on the first line of
        #  synthetic data (shapes required to use the SavedModel format)

        # TODO improve when single format is used
        if transform_def:
            try:
                model.predict(
                    transform_def(
                        tf.data.Dataset.from_tensors(
                            (*x.synthetic.iloc[:1].values.transpose(),)
                        ),
                        features=x.type_metadata["features"],
                    )
                )
            except AttributeError:
                (x_train, y_train), (x_test, y_test) = x.synthetic
                model.predict(
                    tf.data.Dataset.from_tensors(x_train[0][None, :, :])
                )
        else:
            try:
                model.predict(
                    tf.data.Dataset.from_tensors(
                        (*x.synthetic.iloc[:1].values.transpose(),)
                    )
                )
            except AttributeError:
                (x_train, y_train), (x_test, y_test) = x.synthetic
                model.predict(
                    tf.data.Dataset.from_tensors(x_train[0][None, :, :])
                )

        saved_model = _save_model(model)

        request = requests.post(
            f"{self.base_url}/fit",
            data=cloudpickle.dumps(
                (
                    transform_def,
                    saved_model,
                    x.id,
                    target_epsilon,
                    non_DP_training,
                    batch_size,
                    dp_l2_norm_clip,
                    dp_noise_multiplier,
                    dp_num_microbatches,
                    tf_seed,
                    kwargs,
                )
            ),
            headers={"Content-Type": "application/octet-stream"},
            cookies=self.cookies,
            verify=self.verify,
        )
        if request.status_code > 200:
            raise Exception(
                f"Error while training the model.\
                             Full Gateway answer was:{request}"
            )
        task_id = request.json()["task"]
        self.poll_training_status(task_id)
        return task_id

    def training_status(self, id):
        """Fetch a dataset from the Sarus Gateway

        Args:
            id (int): id of the task to be queried. It was provided by the fit
            method

        Returns:
            a string with the status of a training tasks
        """

        request = requests.get(
            f"{self.base_url}/tasks/{id}",
            cookies=self.cookies,
            verify=self.verify,
        )
        return request.json()

    def poll_training_status(self, id, timeout=1000):
        """Poll & display the status of a training task

        Args:
            id (int): id of the task to be queried. It was provided by the fit
            method
            timeout (int): in seconds

        Returns:
            nothing, just display status
        """

        offset = 0
        elapsed_time = 0.0
        while elapsed_time < timeout:
            elapsed_time += 0.5
            request = requests.get(
                f"{self.base_url}/tasks/{id}",
                params=dict(offset=offset),
                cookies=self.cookies,
                verify=self.verify,
            )
            response_dict = request.json()
            offset = response_dict.get("next_offset", 0)
            if "progress" in response_dict:
                progress = base64.b64decode(
                    response_dict["progress"].encode("ascii")
                ).decode("ascii")
                if progress:
                    sys.stdout.write(progress)
            else:
                # this is the end of the training
                sys.stdout.write("\n")
                break
            sys.stdout.flush()
            time.sleep(0.5)

    def fetch_model(self, id):
        """Fetch a trained model from the Sarus Gateway

        Args:
            id (int): id of the task to be queried. It was provided by the fit
            method

        Returns:
            a Keras model
        """

        response = requests.get(
            f"{self.base_url}/models/{id}",
            cookies=self.cookies,
            verify=self.verify,
        )
        # apparently we need to save to a temp file
        # https://github.com/keras-team/keras/issues/9343
        with tempfile.TemporaryDirectory() as _dir:
            f = tarfile.open(fileobj=io.BytesIO(response.content), mode="r:gz")
            f.extractall(_dir)

            return tf.keras.models.load_model(_dir)


def _save_model(model):
    with tempfile.TemporaryDirectory() as _dir:
        model.save(_dir)
        with tempfile.TemporaryDirectory() as _second_dir:
            path = os.path.join(_second_dir, "tmpzip")
            with tarfile.open(path, mode="w:gz") as archive:
                archive.add(_dir, recursive=True, arcname="")
            with open(path, "rb") as f:
                ret = f.read()
                return ret
