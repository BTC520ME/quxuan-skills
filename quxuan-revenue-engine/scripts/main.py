#!/usr/bin/env python3
"""
Quxuan Revenue Engine - 趣选收益引擎
Enterprise-grade AI revenue optimization engine.
企业级AI收益优化引擎。
Version: 2.1.0 (Enterprise)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any

from enterprise import (
    InputSanitizer, RateLimiter, SecurityHeaders, CrossPromotionEngine,
    LLMCaller, LLMCallError, QuxuanLogger, AtomicFileWriter, ErrorCode
)

logger = QuxuanLogger.setup("quxuan-revenue-engine")

# ============================================================
# LLM Integration Layer (thin wrapper around shared LLMCaller)
# ============================================================

SYSTEM_PROMPT = "You are a senior revenue analyst and business strategist. Provide data-driven insights and actionable recommendations. Output in bilingual format (English + Chinese) when appropriate."


def call_llm(prompt: str, provider: str = "dashscope") -> str:
    """
    Call LLM API via shared LLMCaller.
    通过共享LLMCaller调用LLM API。
    """
    return LLMCaller.call(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=prompt,
        provider=provider,
        temperature=0.6,
        max_tokens=6000
    )


# ============================================================
# Dynamic Pricing Module 动态定价模块
# ============================================================

class DynamicPricingEngine:
    """
    Dynamic pricing engine with time-based coefficients.
    基于时段系数的动态定价引擎。
    """
    
    # Hourly pricing coefficients (0-23)
    HOURLY_COEFFICIENTS = [
        0.6, 0.5, 0.5, 0.5, 0.5, 0.6,  # 0-5: late night discount
        0.8, 1.0, 1.2, 1.3, 1.2, 1.1,  # 6-11: morning ramp-up
        1.0, 1.1, 1.2, 1.3, 1.4, 1.5,  # 12-17: afternoon peak
        1.4, 1.3, 1.2, 1.1, 0.9, 0.7   # 18-23: evening decline
    ]
    
    # Weekend coefficients (Sat=1.3, Sun=1.2)
    WEEKEND_COEFFICIENTS = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    WEEKEND_COEFFICIENTS[5] = 1.3  # Saturday
    WEEKEND_COEFFICIENTS[6] = 1.2  # Sunday
    
    # Holiday coefficient
    HOLIDAY_COEFFICIENT = 1.5
    
    def calculate_price(self, base_price: float, timestamp: datetime, 
                       is_holiday: bool = False) -> Dict[str, Any]:
        """
        Calculate dynamic price based on time and demand.
        根据时间和需求计算动态价格。
        """
        hour = timestamp.hour
        weekday = timestamp.weekday()
        
        hourly_coeff = self.HOURLY_COEFFICIENTS[hour]
        day_coeff = self.WEEKEND_COEFFICIENTS[weekday]
        holiday_coeff = self.HOLIDAY_COEFFICIENT if is_holiday else 1.0
        
        final_coeff = hourly_coeff * day_coeff * holiday_coeff
        final_price = round(base_price * final_coeff, 2)
        
        return {
            "base_price": base_price,
            "final_price": final_price,
            "coefficient": round(final_coeff, 3),
            "breakdown": {
                "hourly": hourly_coeff,
                "day_of_week": day_coeff,
                "holiday": holiday_coeff
            },
            "timestamp": timestamp.isoformat(),
            "discount_applied": final_coeff < 1.0,
            "premium_applied": final_coeff > 1.2
        }
    
    def generate_pricing_strategy(self, base_price: float, 
                                  data: Dict = None,
                                  provider: str = "dashscope") -> str:
        """
        Generate comprehensive pricing strategy using LLM.
        使用LLM生成综合定价策略。
        """
        prompt = f"""You are a revenue optimization expert. Based on the following pricing data,
generate a detailed dynamic pricing strategy in both English and Chinese.

Base price: ¥{base_price}
Current time-based coefficient analysis:
- Peak hours (12-17): 1.0-1.5x multiplier
- Off-peak hours (0-5): 0.5-0.6x multiplier  
- Weekend premium: 1.2-1.3x
- Holiday premium: 1.5x

Please provide:
1. Recommended pricing tiers (3-5 tiers)
2. Peak/off-peak strategy
3. Flash sale recommendations
4. Bundle pricing suggestions
5. Expected revenue impact

用中文和英文双语输出策略建议。"""

        return call_llm(prompt, provider=provider)


# ============================================================
# Conversion Funnel Module 转化漏斗模块
# ============================================================

class ConversionFunnelAnalyzer:
    """
    Analyze conversion funnels and identify optimization opportunities.
    分析转化漏斗并识别优化机会。
    """
    
    DEFAULT_FUNNEL_STAGES = [
        "landing_page",    # 落地页
        "browse",          # 浏览
        "add_to_cart",     # 加入购物车
        "checkout_start",  # 开始结算
        "payment",         # 支付
        "completed"        # 完成
    ]
    
    def analyze(self, data: Dict[str, int]) -> Dict[str, Any]:
        """
        Analyze funnel performance.
        分析漏斗表现。
        
        Args:
            data: Dict mapping stage name to user count
        """
        stages = list(data.keys())
        if not stages:
            return {"error": "No funnel data provided"}
        
        initial_count = data[stages[0]]
        analysis = {
            "stages": [],
            "overall_conversion": 0,
            "worst_dropoff": {"stage": "", "rate": 0},
            "recommendations": []
        }
        
        for i, stage in enumerate(stages):
            count = data[stage]
            stage_rate = (count / initial_count * 100) if initial_count > 0 else 0
            
            dropoff = 0
            if i > 0:
                prev_count = data[stages[i-1]]
                dropoff = ((prev_count - count) / prev_count * 100) if prev_count > 0 else 0
            
            stage_info = {
                "name": stage,
                "users": count,
                "rate_from_start": round(stage_rate, 2),
                "dropoff_from_prev": round(dropoff, 2)
            }
            analysis["stages"].append(stage_info)
            
            if dropoff > analysis["worst_dropoff"]["rate"]:
                analysis["worst_dropoff"] = {"stage": stage, "rate": dropoff}
        
        if initial_count > 0:
            final_count = data[stages[-1]]
            analysis["overall_conversion"] = round(final_count / initial_count * 100, 2)
        
        return analysis
    
    def generate_optimization_report(self, data: Dict[str, int],
                                     provider: str = "dashscope") -> str:
        """Generate LLM-powered optimization report."""
        analysis = self.analyze(data)
        
        prompt = f"""You are a conversion rate optimization expert. Analyze this funnel data
and provide actionable recommendations in both English and Chinese:

Funnel Analysis:
{json.dumps(analysis, indent=2, ensure_ascii=False)}

Please provide:
1. Top 3 drop-off points and why they occur
2. Specific optimization tactics for each drop-off
3. A/B test recommendations
4. Expected conversion improvement estimates
5. Quick wins vs long-term strategies

请用中文和英文双语输出优化建议。"""

        return call_llm(prompt, provider=provider)


# ============================================================
# A/B Testing Module A/B测试模块
# ============================================================

class ABTestDesigner:
    """
    A/B testing framework with statistical rigor.
    具备统计严谨性的A/B测试框架。
    """
    
    @staticmethod
    def calculate_sample_size(baseline_rate: float, effect_size: float,
                             alpha: float = 0.05, power: float = 0.8) -> int:
        """
        Calculate required sample size per variant.
        计算每个变体所需的样本量。
        """
        import math
        
        # Z-scores for alpha=0.05 (two-tailed) and power=0.8
        z_alpha = 1.96
        z_beta = 0.84
        
        p1 = baseline_rate
        p2 = baseline_rate * (1 + effect_size)
        
        pooled_p = (p1 + p2) / 2
        
        numerator = (z_alpha * math.sqrt(2 * pooled_p * (1 - pooled_p)) + 
                    z_beta * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
        denominator = (p2 - p1) ** 2
        
        if denominator == 0:
            return 0
            
        return math.ceil(numerator / denominator)
    
    @staticmethod
    def analyze_results(control_conversions: int, control_total: int,
                       variant_conversions: int, variant_total: int) -> Dict[str, Any]:
        """
        Analyze A/B test results with statistical significance.
        分析A/B测试结果及统计显著性。
        """
        import math
        
        control_rate = control_conversions / control_total if control_total > 0 else 0
        variant_rate = variant_conversions / variant_total if variant_total > 0 else 0
        
        # Z-test for two proportions
        pooled_p = (control_conversions + variant_conversions) / (control_total + variant_total)
        
        if pooled_p == 0 or pooled_p == 1:
            z_score = 0
        else:
            se = math.sqrt(pooled_p * (1 - pooled_p) * (1/control_total + 1/variant_total))
            z_score = (variant_rate - control_rate) / se if se > 0 else 0
        
        # Approximate p-value (two-tailed)
        p_value = 2 * (1 - 0.5 * (1 + math.erf(abs(z_score) / math.sqrt(2))))
        
        lift = ((variant_rate - control_rate) / control_rate * 100) if control_rate > 0 else 0
        
        return {
            "control_rate": round(control_rate * 100, 2),
            "variant_rate": round(variant_rate * 100, 2),
            "lift_percent": round(lift, 2),
            "z_score": round(z_score, 4),
            "p_value": round(p_value, 4),
            "significant": p_value < 0.05,
            "recommendation": "Ship variant" if p_value < 0.05 and lift > 0 else "Keep control" if p_value >= 0.05 else "Variant is worse"
        }


# ============================================================
# Retention Scoring Module 留存评分模块
# ============================================================

class RetentionScorer:
    """
    User retention risk scoring and LTV prediction.
    用户留存风险评分与LTV预测。
    """
    
    # Risk factors and weights
    RISK_FACTORS = {
        "days_since_last_active": {"weight": 0.3, "thresholds": {3: 0.1, 7: 0.3, 14: 0.6, 30: 0.9}},
        "login_frequency_7d": {"weight": 0.2, "thresholds": {0: 0.9, 1: 0.6, 3: 0.3, 7: 0.0}},
        "avg_session_duration": {"weight": 0.15, "thresholds": {1: 0.8, 5: 0.5, 15: 0.2, 30: 0.0}},
        "purchases_last_30d": {"weight": 0.2, "thresholds": {0: 0.7, 1: 0.3, 3: 0.1, 5: 0.0}},
        "support_tickets_30d": {"weight": 0.15, "thresholds": {0: 0.0, 1: 0.3, 3: 0.6, 5: 0.9}}
    }
    
    def calculate_risk_score(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate churn risk score (0-100, higher = more risky).
        计算流失风险评分（0-100，越高越危险）。
        """
        total_score = 0
        factor_scores = {}
        
        for factor, config in self.RISK_FACTORS.items():
            value = user_data.get(factor, 0)
            weight = config["weight"]
            
            # Find appropriate score from thresholds
            thresholds = config["thresholds"]
            score = 0
            for threshold, s in sorted(thresholds.items()):
                if value >= threshold:
                    score = s
            
            weighted_score = score * weight
            total_score += weighted_score
            factor_scores[factor] = {
                "value": value,
                "raw_score": round(score, 2),
                "weighted_score": round(weighted_score, 2)
            }
        
        risk_level = "low" if total_score < 0.3 else "medium" if total_score < 0.6 else "high"
        
        return {
            "risk_score": round(total_score * 100, 1),
            "risk_level": risk_level,
            "factor_scores": factor_scores,
            "recommended_actions": self._get_actions(risk_level, user_data)
        }
    
    def predict_ltv(self, user_data: Dict[str, Any], avg_monthly_spend: float) -> Dict[str, Any]:
        """
        Predict customer lifetime value.
        预测客户终身价值。
        """
        risk_score = self.calculate_risk_score(user_data)
        
        # Estimate remaining lifetime in months based on risk
        monthly_churn_prob = risk_score["risk_score"] / 100
        if monthly_churn_prob >= 1:
            expected_months = 1
        elif monthly_churn_prob <= 0:
            expected_months = 60  # Very low churn, cap at 5 years
        else:
            expected_months = 1 / monthly_churn_prob  # Geometric distribution: E[lifetime] = 1/p
        
        expected_months = min(expected_months, 60)  # Cap at 5 years
        ltv = avg_monthly_spend * expected_months
        
        return {
            "predicted_ltv": round(ltv, 2),
            "expected_lifetime_months": round(expected_months, 1),
            "avg_monthly_spend": avg_monthly_spend,
            "churn_probability": round(monthly_churn_prob, 3),
            "confidence": "medium"  # Would need more data for high confidence
        }
    
    def _get_actions(self, risk_level: str, user_data: Dict) -> List[str]:
        """Get recommended retention actions based on risk level."""
        actions = {
            "high": [
                "Send personalized win-back email with special offer",
                "Trigger push notification with exclusive discount",
                "Assign customer success manager for outreach",
                "发送个性化召回邮件+特别优惠",
                "推送专属折扣通知",
                "安排客户成功经理主动联系"
            ],
            "medium": [
                "Send engagement-nudge notification",
                "Offer loyalty points bonus",
                "Recommend relevant new features/content",
                "发送促活通知",
                "提供积分奖励",
                "推荐相关新功能/内容"
            ],
            "low": [
                "Continue normal engagement flow",
                "Monitor for behavior changes",
                "保持正常互动流程",
                "关注行为变化"
            ]
        }
        return actions.get(risk_level, actions["low"])


# ============================================================
# Revenue Dashboard 收益仪表盘
# ============================================================

class RevenueDashboard:
    """
    Generate revenue reports and dashboards.
    生成收益报告和仪表盘。
    """
    
    def generate_report(self, data: Dict[str, Any], period: str = "monthly",
                        provider: str = "dashscope") -> str:
        """
        Generate comprehensive revenue report using LLM.
        使用LLM生成综合收益报告。
        """
        prompt = f"""You are a senior revenue analyst. Generate a comprehensive revenue report
for period: {period}. Use the following data and provide insights in both English and Chinese.

Data:
{json.dumps(data, indent=2, ensure_ascii=False)}

Report should include:
1. Executive Summary 执行摘要
2. Key Metrics (ARPU, LTV, CAC, Churn Rate) 关键指标
3. Revenue Trends 收益趋势
4. Top Performing Segments 最佳表现细分
5. Risk Areas 风险区域
6. Actionable Recommendations 可执行建议
7. Next Period Forecast 下期预测

Format as a professional Markdown report with bilingual headings.
请以专业的Markdown格式输出，标题使用双语。"""

        return call_llm(prompt, provider=provider)


# ============================================================
# Main Handler 主处理函数
# ============================================================

def handle_request(mode: str, data_path: str = None, output: str = None,
                  period: str = "monthly", provider: str = "dashscope",
                  **kwargs) -> str:
    """
    Main request handler - routes to appropriate module.
    主请求处理器 - 路由到相应模块。
    """
    # Load data if provided
    data = {}
    if data_path:
        if not os.path.exists(data_path):
            return json.dumps({"error": f"数据文件不存在 / Data file not found: {data_path}"})
        if os.path.getsize(data_path) > 5 * 1024 * 1024:  # 5MB limit
            return json.dumps({"error": "数据文件过大(>5MB)，请拆分后重试 / Data file too large (>5MB)"})
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except UnicodeDecodeError:
            return json.dumps({"error": "数据文件编码错误，请使用UTF-8格式 / File encoding error"})
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"数据文件JSON格式错误 / Invalid JSON: {str(e)[:100]}"})
        except PermissionError:
            return json.dumps({"error": f"无权限读取文件 / Permission denied: {data_path}"})
        except Exception as e:
            return json.dumps({"error": f"读取数据失败 / Failed to load data: {str(e)[:100]}"})
    
    # 校验 data 类型必须为 dict
    if not isinstance(data, dict):
        return json.dumps({"error": "数据文件必须包含一个JSON对象(字典) / Data file must contain a JSON object (dict)"})

    result = ""
    
    if mode == "pricing":
        engine = DynamicPricingEngine()
        base_price = data.get("base_price", 100)
        result = engine.generate_pricing_strategy(base_price, data, provider=provider)
    
    elif mode == "funnel":
        analyzer = ConversionFunnelAnalyzer()
        result = analyzer.generate_optimization_report(data, provider=provider)
    
    elif mode == "ab_test":
        designer = ABTestDesigner()
        baseline = float(kwargs.get("baseline", 100))
        effect = float(kwargs.get("effect_size", 0.15))
        sample_size = designer.calculate_sample_size(baseline / 100, effect)
        result = f"""A/B Test Design 测试设计:
- Baseline conversion rate 基准转化率: {baseline}%
- Minimum detectable effect 最小可检测效应: {effect*100}%
- Required sample size per variant 每个变体所需样本量: {sample_size:,}
- Total sample needed 总需样本量: {sample_size*2:,}
- Estimated duration (at 1000 daily users): {sample_size*2/1000:.0f} days

Statistical parameters 统计参数:
- Alpha (α): 0.05 (two-tailed)
- Power (1-β): 0.80
- Confidence level 置信水平: 95%
"""
    
    elif mode == "retention":
        scorer = RetentionScorer()
        raw_users = data.get("users", None) if data else None
        if raw_users is not None and not isinstance(raw_users, list):
            return json.dumps({"error": "users 字段必须是数组 / users field must be an array"})
        users = raw_users if raw_users else [data]
        results = []
        for user in users[:100]:  # Limit to 100 users
            if not isinstance(user, dict):
                continue
            risk = scorer.calculate_risk_score(user)
            ltv = scorer.predict_ltv(user, data.get("avg_monthly_spend", 50))
            results.append({**risk, "ltv": ltv})
        result = json.dumps(results, indent=2, ensure_ascii=False)
    
    elif mode == "dashboard":
        dashboard = RevenueDashboard()
        result = dashboard.generate_report(data, period, provider=provider)
    
    else:
        result = f"Unknown mode: {mode}. Available modes: pricing, funnel, ab_test, retention, dashboard"
    
    # Output result
    if output:
        try:
            AtomicFileWriter.write(output, result)
            return f"✅ Result saved to {output}"
        except PermissionError:
            return json.dumps({"error": f"无权限写入文件 / Permission denied: {output}"})
        except OSError as e:
            return json.dumps({"error": f"写入文件失败 / Write failed: {str(e)[:100]}"})
    
    return result


# ============================================================
# CLI Entry Point 命令行入口
# ============================================================


class FriendlyParser(argparse.ArgumentParser):
    """友好错误提示 - 双语输出"""
    def error(self, message):
        print(f"❌ 参数错误 / Argument Error: {message}\n", file=sys.stderr)
        print(f"💡 使用 --help 查看完整用法 / Use --help for usage", file=sys.stderr)
        sys.exit(2)

def main():
    parser = FriendlyParser(
        description="Quxuan Revenue Engine 趣选收益引擎 - AI-powered revenue optimization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples 示例:
  # Dynamic pricing analysis 动态定价
  python main.py --mode pricing --data revenue.json

  # Funnel optimization 漏斗优化
  python main.py --mode funnel --data journey.json

  # A/B test design 测试设计
  python main.py --mode ab_test --baseline 10 --effect_size 0.15

  # Retention scoring 留存评分
  python main.py --mode retention --data users.json

  # Revenue dashboard 收益仪表盘
  python main.py --mode dashboard --data metrics.json --period monthly
        """
    )
    
    parser.add_argument("--version", action="version", version="趣选收益引擎 Quxuan Revenue Engine v2.1.0")
    parser.add_argument("--mode", required=True, 
                       choices=["pricing", "funnel", "ab_test", "retention", "dashboard"],
                       help="Analysis mode 分析模式")
    parser.add_argument("--data", help="Input data file path (JSON) 输入数据文件路径")
    parser.add_argument("--output", help="Output file path 输出文件路径")
    parser.add_argument("--period", default="monthly", choices=["daily", "weekly", "monthly"],
                       help="Report period 报告周期")
    parser.add_argument("--provider", default="dashscope", 
                       choices=["dashscope", "openai", "deepseek"],
                       help="LLM provider")
    parser.add_argument("--baseline", default="10", help="Baseline conversion rate (percent) for A/B test")
    parser.add_argument("--effect_size", default="0.15", help="Minimum detectable effect for A/B test")
    
    args = parser.parse_args()
    
    # === 企业级限流检查 ===
    rate_limiter = RateLimiter(max_requests=100, window_seconds=3600)
    user_key = SecurityHeaders.hash_content(os.getenv("USER", "anonymous"))
    if not rate_limiter.is_allowed(user_key):
        print("⚠️ 请求频率过高，请稍后再试 / Rate limit exceeded, please try again later", file=sys.stderr)
        sys.exit(1)
    
    # === 企业级输入清洗 ===
    if args.data:
        valid, err = InputSanitizer.validate(args.data, "data path")
        if not valid:
            print(f"❌ 输入错误: {err}", file=sys.stderr)
            sys.exit(1)
    
    try:
        result = handle_request(
            mode=args.mode,
            data_path=args.data,
            output=args.output,
            period=args.period,
            provider=args.provider,
            baseline=args.baseline,
            effect_size=args.effect_size
        )
    except Exception as e:
        print(f"❌ 执行失败: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 检查是否返回了错误 JSON
    try:
        parsed = json.loads(result)
        if isinstance(parsed, dict) and "error" in parsed:
            print(f"❌ 执行错误 / Error: {parsed['error']}", file=sys.stderr)
            sys.exit(1)
    except (json.JSONDecodeError, TypeError):
        pass  # 非 JSON 结果，正常输出
    
    print(result)
    
    # 追加交叉推荐（仅控制台输出时）
    if not args.output:
        print(CrossPromotionEngine.get_recommendation("quxuan-revenue-engine"))
        print(CrossPromotionEngine.get_closing_banner("quxuan-revenue-engine"))


if __name__ == "__main__":
    main()
