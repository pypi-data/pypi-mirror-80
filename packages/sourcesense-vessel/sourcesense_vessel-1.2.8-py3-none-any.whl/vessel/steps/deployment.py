import requests
import uuid
import os
import textwrap
import json
import subprocess
import urllib
from typing import List, Callable, Tuple
from vessel.pipeline import Step, Payload
from vessel.logging import logger
from vessel.version import LATEST_AGENT, LATEST_SENTINEL
from vessel.utilities import sanitizeClusterName
class DeployAgentStep(Step):
  """
  Deploy Agent
  """
  def __init__(self):
    super().__init__()

  def run(self, payload:Payload, start_fn:Callable, end_fn:Callable, prompt_fn:Callable) -> Payload:
    start_fn("Deploying agent")
    yaml = os.path.expanduser(f"~/.daas/{payload.token}/agent.yaml")
    bashCommand = f"kubectl -n daas apply -f {yaml}"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
      raise Exception(error)
    for out in output.decode('utf-8').split("\n"):
      end_fn(out)
    return payload

class DeploySentinelStep(Step):
  """
  Generate kube deployments for agent & sentinel
  """

  def __init__(self):
    super().__init__()

  def run(self, payload:Payload, start_fn:Callable, end_fn:Callable, prompt_fn:Callable) -> Payload:
    start_fn("Deploying sentinel")
    yaml = os.path.expanduser(f"~/.daas/{payload.token}/sentinel.yaml")
    bashCommand = f"kubectl -n daas apply -f {yaml}"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
      raise Exception(error)
    for out in output.decode('utf-8').split("\n"):
      end_fn(out)
    return payload

class GenerateYamlStep(Step):
  """
  Generate kube deployments for agent & sentinel
  """

  def __init__(self):
    super().__init__()

  def _get_keys(self, payload:Payload) -> Tuple[str]:
    if payload.rsa:
      name = sanitizeClusterName(payload.cluster['result']['name'])
      return (name, payload.rsa, payload.vault_user, payload.vault_pwd, payload.distribution)
    else:
      with open(os.path.expanduser(f"~/.daas/{payload.token}/registration.json"), 'r') as f:
        registration = json.load(f)
      with open(os.path.expanduser(f"~/.daas/vault.json"), 'r') as f:
        vault = json.load(f)
      
      name = sanitizeClusterName(registration['cluster']['result']['name'])
      return (name, registration['rsa'], vault['public']['user'], vault['public']['pwd'], registration['distribution'])



  def run(self, payload:Payload, start_fn:Callable, end_fn:Callable, prompt_fn:Callable) -> Payload:
    start_fn("Loading keys")
    path = os.path.expanduser(f"~/.daas/{payload.token}")
    
    (name, rsa, vault_user, vault_pwd, distribution) = self._get_keys(payload)

    start_fn("generating sentinel yaml")
    sentinel_yaml = self.sentinel_yaml(name=name, token=payload.token, vault_password=vault_pwd, distribution=distribution, tag=LATEST_SENTINEL)
    
    with open(f"{path}/sentinel.yaml", 'w') as f:
      f.write(sentinel_yaml)

    start_fn("generating agent yaml")
    agent_yaml = self.agent_yaml(name=name, token=payload.token, rsa=rsa.replace("\n", "\\n"), tag=LATEST_AGENT)
   
    with open(f"{path}/agent.yaml", 'w') as f:
      f.write(agent_yaml)
    
    payload.agent_yaml = agent_yaml
    payload.sentinel_yaml = sentinel_yaml
    end_fn("OK")

    return payload


  def sentinel_yaml(self, **kwargs):
    """
    Output the deployemnt for the Sentinel
    """
    return textwrap.dedent(
        """\
        apiVersion: v1
        kind: List
        metadata:
          resourceVersion: ""
          selfLink: ""
        items:
        - apiVersion: v1
          kind: Secret
          metadata:
            name: vault-secret
          type: Opaque
          stringData:
            HOST: "http://vault.vault:8200"
            USER: "sourcesense"
            PWD: "{vault_password}"
        - apiVersion: v1
          kind: ConfigMap
          metadata:
            name: {name}-sentinel-tasks-cm
          data:
            tasks.json: |
              {{
                "tasks": [
                  {{
                    "name": "kubelinter",
                    "module": "sentinel.tasks.kubelinter.KubeLinter",
                    "enabled": true,
                    "scheduled": 3600
                  }},
                  {{
                    "name": "kubecounter",
                    "module": "sentinel.tasks.kubecounter.KubeCounter",
                    "enabled": true,
                    "scheduled": 3600
                  }},
                  {{
                    "name": "anchore",
                    "module": "sentinel.tasks.anchore.Anchore",
                    "enabled": true,
                    "scheduled": 3600
                  }},
                  {{
                    "name": "events",
                    "module": "sentinel.tasks.events.Events",
                    "enabled": true
                  }}
                ]
              }}
        - apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: {name}-sentinel
          spec:
            selector:
              matchLabels:
                app: {name}-sentinel
            replicas: 1
            template:
              metadata:
                name: {name}-sentinel
                labels:
                  app: {name}-sentinel
              spec:
                volumes:
                  - name: tasks-volume
                    configMap:
                      name: {name}-sentinel-tasks-cm
                containers:
                - name: {name}-sentinel
                  image: docker-registry.oc.corp.sourcesense.com/daas/workstation-sentinel:{tag}
                  volumeMounts:
                    - name: tasks-volume
                      mountPath: /etc/custom
                  env:
                  - name: CLUSTER_TOKEN
                    value: {token}
                  - name: TASKS_JSON
                    value: /etc/custom/tasks.json 
                  - name: KUBE_DISTRIBUTION
                    value: {distribution}
                  - name: VAULT_HOST
                    valueFrom:
                      secretKeyRef:
                        name: vault-secret
                        key: HOST
                  - name: VAULT_USER
                    valueFrom:
                      secretKeyRef:
                        name: vault-secret
                        key: USER
                  - name: VAULT_PWD
                    valueFrom:
                      secretKeyRef:
                        name: vault-secret
                        key: PWD
                  - name: ANCHORE_URL
                    value: http://anchore-anchore-engine-api.anchore.svc:8228
                  - name: ANCHORE_USERNAME
                    value: admin
                  - name: ANCHORE_PWD
                    valueFrom:
                      secretKeyRef:
                        name: anchore-password
                        key: ANCHORE_PWD
                  - name: BEAT_OUTPUT
                    value: filebeat.daas.svc:9000
                imagePullSecrets:
                - name: sourcesense-registry
        - apiVersion: v1
          kind: Service
          metadata:
            labels:
              app: {name}-sentinel
            name: {name}-sentinel
          spec:
            ports:
            - name: 8089-tcp
              port: 8089
              protocol: TCP
              targetPort: 8089
            selector:
              app: {name}-sentinel
            sessionAffinity: None
            type: ClusterIP
        - apiVersion: extensions/v1beta1
          kind: Ingress
          metadata:
            name: {name}-sentinel-ingress
          spec:
            rules:
            - host: {name}-sentinel.local
              http:
                paths:
                - backend:
                    serviceName: {name}-sentinel
                    servicePort: 8089
                  path: /
        """
        ).format(**kwargs)


  def agent_yaml(self, **kwargs):
    """
    Output the deployemnt and secret for the agent
    """
    return textwrap.dedent(
        """\
        apiVersion: v1
        kind: List
        metadata:
          resourceVersion: ""
          selfLink: ""
        items:
        - apiVersion: v1
          kind: Secret
          metadata:
            name: {name}-secrets
          type: Opaque
          stringData:
            PRIVATE_KEY: "{rsa}"
        - apiVersion: apps/v1
          kind: Deployment
          metadata:
            name: {name}-agent
          spec:
            selector:
              matchLabels:
                app: {name}-agent
            replicas: 1
            template:
              metadata:
                labels:
                  app: {name}-agent
              spec:
                containers:
                - name: {name}-agent
                  image: docker-registry.oc.corp.sourcesense.com/daas/workstation-agent:{tag}
                  env:
                  - name: CLUSTER_TOKEN
                    value: {token}
                  - name: VAULT_HOST
                    valueFrom:
                      secretKeyRef:
                        name: vault-secret
                        key: HOST
                  - name: VAULT_USER
                    valueFrom:
                      secretKeyRef:
                        name: vault-secret
                        key: USER
                  - name: VAULT_PWD
                    valueFrom:
                      secretKeyRef:
                        name: vault-secret
                        key: PWD
                  - name: PRIVATE_KEY
                    valueFrom:
                      secretKeyRef:
                        name: {name}-secrets
                        key: PRIVATE_KEY
                imagePullSecrets:
                - name: sourcesense-registry


        """
        ).format(**kwargs)