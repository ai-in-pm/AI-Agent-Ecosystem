from typing import Dict, Any, List
from datetime import datetime, timedelta
from core.base_agent import BaseAgent

class UserOnboardingAgent(BaseAgent):
    """Agent responsible for user onboarding and initial experience optimization."""
    
    async def initialize(self) -> bool:
        """Initialize user onboarding systems."""
        self.onboarding_flows = {
            "default": {
                "steps": [
                    "welcome",
                    "feature_overview",
                    "first_agent",
                    "marketplace_intro",
                    "support_resources"
                ],
                "completion_reward": "premium_trial"
            },
            "developer": {
                "steps": [
                    "welcome",
                    "api_overview",
                    "sdk_setup",
                    "first_integration",
                    "documentation"
                ],
                "completion_reward": "api_credits"
            },
            "enterprise": {
                "steps": [
                    "welcome",
                    "enterprise_features",
                    "team_setup",
                    "security_overview",
                    "support_channels"
                ],
                "completion_reward": "consultation"
            }
        }
        
        self.user_progress = {}
        self.conversion_metrics = {}
        return True
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute onboarding-related tasks."""
        if task["type"] == "start_onboarding":
            return await self._start_onboarding(
                user_id=task["user_id"],
                flow_type=task.get("flow_type", "default")
            )
        elif task["type"] == "track_progress":
            return await self._track_progress(
                user_id=task["user_id"],
                step=task["step"]
            )
        elif task["type"] == "optimize_flow":
            return await self._optimize_flow(flow_type=task["flow_type"])
            
        return {"status": "error", "message": "Unknown task type"}
    
    async def monitor(self) -> Dict[str, Any]:
        """Monitor onboarding effectiveness and user progress."""
        completion_rates = self._calculate_completion_rates()
        conversion_metrics = await self._gather_conversion_metrics()
        
        return {
            "completion_rates": completion_rates,
            "conversion_metrics": conversion_metrics,
            "active_users": len(self.user_progress),
            "last_check": datetime.utcnow().isoformat()
        }
    
    async def _start_onboarding(
        self,
        user_id: str,
        flow_type: str = "default"
    ) -> Dict[str, Any]:
        """Start onboarding process for new user."""
        if flow_type not in self.onboarding_flows:
            return {"status": "error", "message": f"Invalid flow type: {flow_type}"}
            
        flow = self.onboarding_flows[flow_type]
        self.user_progress[user_id] = {
            "flow_type": flow_type,
            "current_step": flow["steps"][0],
            "completed_steps": [],
            "start_time": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat()
        }
        
        first_step = await self._prepare_step(user_id, flow["steps"][0])
        return {
            "status": "success",
            "user_id": user_id,
            "flow_type": flow_type,
            "first_step": first_step
        }
    
    async def _track_progress(
        self,
        user_id: str,
        step: str
    ) -> Dict[str, Any]:
        """Track user's progress through onboarding."""
        if user_id not in self.user_progress:
            return {"status": "error", "message": "User not found"}
            
        progress = self.user_progress[user_id]
        flow = self.onboarding_flows[progress["flow_type"]]
        
        if step not in flow["steps"]:
            return {"status": "error", "message": "Invalid step"}
            
        # Update progress
        progress["completed_steps"].append(progress["current_step"])
        current_index = flow["steps"].index(step)
        
        if current_index + 1 < len(flow["steps"]):
            progress["current_step"] = flow["steps"][current_index + 1]
            next_step = await self._prepare_step(user_id, progress["current_step"])
        else:
            next_step = await self._complete_onboarding(user_id)
            
        progress["last_activity"] = datetime.utcnow().isoformat()
        
        return {
            "status": "success",
            "user_id": user_id,
            "completed_step": step,
            "next_step": next_step
        }
    
    async def _optimize_flow(
        self,
        flow_type: str
    ) -> Dict[str, Any]:
        """Optimize onboarding flow based on user data."""
        if flow_type not in self.onboarding_flows:
            return {"status": "error", "message": f"Invalid flow type: {flow_type}"}
            
        metrics = await self._analyze_flow_metrics(flow_type)
        optimizations = self._generate_flow_optimizations(flow_type, metrics)
        
        if optimizations["changes"]:
            await self._apply_flow_optimizations(flow_type, optimizations["changes"])
            
        return {
            "status": "success",
            "flow_type": flow_type,
            "metrics": metrics,
            "optimizations": optimizations
        }
    
    def _calculate_completion_rates(self) -> Dict[str, float]:
        """Calculate completion rates for each flow type."""
        completion_rates = {}
        for flow_type in self.onboarding_flows:
            users = [u for u in self.user_progress.values() if u["flow_type"] == flow_type]
            if users:
                completed = sum(
                    1 for u in users
                    if len(u["completed_steps"]) == len(self.onboarding_flows[flow_type]["steps"])
                )
                completion_rates[flow_type] = completed / len(users)
            else:
                completion_rates[flow_type] = 0.0
        return completion_rates
    
    async def _gather_conversion_metrics(self) -> Dict[str, Any]:
        """Gather conversion metrics for onboarding flows."""
        metrics = {}
        for flow_type in self.onboarding_flows:
            if flow_type in self.conversion_metrics:
                metrics[flow_type] = {
                    "conversion_rate": self.conversion_metrics[flow_type].get("rate", 0.0),
                    "average_time": self.conversion_metrics[flow_type].get("avg_time", 0.0),
                    "drop_off_points": self.conversion_metrics[flow_type].get("drop_offs", {})
                }
        return metrics
    
    async def _prepare_step(
        self,
        user_id: str,
        step: str
    ) -> Dict[str, Any]:
        """Prepare content and actions for onboarding step."""
        step_content = await self._generate_step_content(step)
        return {
            "step": step,
            "content": step_content,
            "actions": self._get_step_actions(step)
        }
    
    async def _complete_onboarding(
        self,
        user_id: str
    ) -> Dict[str, Any]:
        """Handle onboarding completion and rewards."""
        progress = self.user_progress[user_id]
        flow = self.onboarding_flows[progress["flow_type"]]
        
        # Grant completion reward
        reward = await self._grant_reward(user_id, flow["completion_reward"])
        
        return {
            "status": "completed",
            "reward": reward,
            "next_steps": await self._generate_next_steps(user_id)
        }
    
    async def _analyze_flow_metrics(
        self,
        flow_type: str
    ) -> Dict[str, Any]:
        """Analyze metrics for specific onboarding flow."""
        users = [u for u in self.user_progress.values() if u["flow_type"] == flow_type]
        
        step_completion = {}
        for step in self.onboarding_flows[flow_type]["steps"]:
            completed = sum(1 for u in users if step in u["completed_steps"])
            step_completion[step] = completed / len(users) if users else 0.0
            
        return {
            "step_completion": step_completion,
            "average_time": self._calculate_average_completion_time(users)
        }
    
    def _generate_flow_optimizations(
        self,
        flow_type: str,
        metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate optimization suggestions for flow."""
        changes = []
        
        # Analyze step completion rates
        for step, rate in metrics["step_completion"].items():
            if rate < 0.7:  # Less than 70% completion
                changes.append({
                    "type": "step_optimization",
                    "step": step,
                    "suggestion": "simplify_content"
                })
                
        return {"changes": changes}
    
    async def _apply_flow_optimizations(
        self,
        flow_type: str,
        changes: List[Dict[str, Any]]
    ) -> None:
        """Apply optimizations to onboarding flow."""
        for change in changes:
            if change["type"] == "step_optimization":
                await self._optimize_step(flow_type, change["step"])
    
    def _calculate_average_completion_time(
        self,
        users: List[Dict[str, Any]]
    ) -> float:
        """Calculate average time to complete onboarding."""
        completed_users = [
            u for u in users
            if len(u["completed_steps"]) == len(self.onboarding_flows[u["flow_type"]]["steps"])
        ]
        
        if not completed_users:
            return 0.0
            
        total_time = sum(
            (datetime.fromisoformat(u["last_activity"]) - 
             datetime.fromisoformat(u["start_time"])).total_seconds()
            for u in completed_users
        )
        
        return total_time / len(completed_users)
    
    async def _generate_step_content(self, step: str) -> Dict[str, Any]:
        """Generate content for onboarding step."""
        # Implementation would include content generation logic
        return {"title": step, "content": f"Content for {step}"}
    
    def _get_step_actions(self, step: str) -> List[str]:
        """Get available actions for onboarding step."""
        # Implementation would include action definition logic
        return ["complete", "skip", "get_help"]
    
    async def _grant_reward(
        self,
        user_id: str,
        reward_type: str
    ) -> Dict[str, Any]:
        """Grant completion reward to user."""
        # Implementation would include reward granting logic
        return {"type": reward_type, "granted": True}
    
    async def _generate_next_steps(
        self,
        user_id: str
    ) -> List[Dict[str, Any]]:
        """Generate recommended next steps after onboarding."""
        # Implementation would include next steps generation logic
        return [
            {"type": "create_agent", "priority": "high"},
            {"type": "explore_marketplace", "priority": "medium"}
        ]
    
    async def _optimize_step(
        self,
        flow_type: str,
        step: str
    ) -> None:
        """Optimize specific onboarding step."""
        # Implementation would include step optimization logic
        pass
