# Week 06: Elastic Load Balancing & Auto Scaling
### Concepts: ALB target groups & health checks, launch templates, Auto Scaling Group scaling policies.


##### LAB Lab 6.1 — ASG behind an ALB (In-progress)
55. EC2 → Launch Templates → Create launch template → name property-api-template, same
AMI/user-data as Week 3's Lab 3.1, instance type t3.micro
56. EC2 → Target Groups → Create target group → instance target type, port 8080, health check
path /health
57. EC2 → Load Balancers → Create Application Load Balancer → internet-facing, span both public
subnets from training-vpc, listener HTTP:80 → forward to the target group above
58. EC2 → Auto Scaling Groups → Create ASG → use property-api-template, attach to the existing
target group, VPC = training-vpc, subnets = both private subnets, desired/min/max = 2/1/4
59. Scaling policy → Target tracking → metric: Average CPU Utilization → target value 50
You'll know it worked when: curl http://<alb-dns-name>/health returns {"status":"ok"} and curl
http://<alb-dns-name>/properties returns the listings — same PropertyLite app from Week 3, now
behind a load balancer with 2 instances instead of 1.


I am having difficulties resolving a bad gateway for this lab. I speculate that it is related to security group rules. I plan on finishing this lab this week. 



##### LAB Lab 6.2 — Prove self-healing and scaling (complete)
Terminate one instance manually via console, then watch:
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-name <your-asg-name>
Watch the Activity tab in the ASG console — a replacement instance should launch within ~1–2 minutes.
To see scaling, SSH into an instance and run a CPU stress test:
sudo amazon-linux-extras install epel -y
sudo yum install -y stress
stress --cpu 2 --timeout 300
You'll know it worked when: CloudWatch shows CPU spiking above 50% and, within a few minutes, the
ASG's desired capacity increases and a new instance appears.
DEBUG Debug Lab 6.3 — ALB returns 502 Bad Gateway
Symptom: the ALB's DNS name loads in your browser but shows “502 Bad Gateway” instead of your
PropertyLite response.
Diagnose it yourself first — check the target group's Targets tab: are the registered instances showing
“healthy” or “unhealthy”? Does the instance's security group have an inbound rule allowing traffic from
the ALB's security group on port 8080? Does the health check path (/health) actually return a 200 on the
instance directly?
Root cause & fix: the near-universal cause here is the instance's security group only allows SSH/8080
from “My IP” (copied straight from Week 3's lab) and was never opened to the ALB's security group. Fix:
edit the instance's security group inbound rules → add custom TCP port 8080 with source = the ALB's
security group ID.
Lesson: an ALB is just another network peer — it needs an explicit inbound rule like anything else,
“internet-facing” doesn't mean “trusted by default.”
CLEANUP
Delete the ASG (this terminates its instances), then the ALB, then the target group, then the launch
template.
DELIVERABLE
week-06/load-test-report.md with CloudWatch screenshots showing the CPU spike and the scale-out
event, plus the timestamp gap between them.

I have completed this lab. As part of my troubleshooting the first lab, I successfully completed instance refreshes and manual deletion of instances, and I watched as the autoscaler rebuilt them with the template.
