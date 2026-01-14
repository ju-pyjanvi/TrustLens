import re

PATTERNS = [
    {
        "name": "Artificial Scarcity",
        "category": "Urgency & Scarcity",
        "regex": re.compile(r"(only\s+\d+(\s+\w+)?\s+left|limited\s+(stock|quantity|availability)|selling\s+fast|almost\s+gone|running\s+out|few\s+remaining|while\s+supplies\s+last|low\s+stock)", re.I),
        "explanation": "Creates pressure by implying limited product availability."
    },
    {
        "name": "Time Pressure",
        "category": "Urgency & Scarcity",
        "regex": re.compile(r"(act\s+now|hurry|offer\s+ends\s+soon|last\s+chance|final\s+(hours|days|sale)|ends\s+tonight|today\s+only|limited\s+time|expires\s+(soon|today|tomorrow)|deadline|don't\s+wait)", re.I),
        "explanation": "Pressures immediate action with time-based urgency."
    },
    {
        "name": "Countdown Pressure",
        "category": "Urgency & Scarcity",
        "regex": re.compile(r"(deal\s+ends\s+in\s+\d+|countdown|time\s+(is\s+)?running\s+out|\d+\s*(hours?|minutes?|days?)\s+(left|remaining)|clock\s+is\s+ticking|before\s+it's\s+too\s+late)", re.I),
        "explanation": "Uses countdown timers to create artificial urgency."
    },
    {
        "name": "Flash Sale",
        "category": "Urgency & Scarcity",
        "regex": re.compile(r"(flash\s+sale|lightning\s+deal|daily\s+deal|deal\s+of\s+the\s+day|one\s+day\s+(only|sale)|24[\s-]?hour\s+sale|weekend\s+only|today'?s\s+deals?)", re.I),
        "explanation": "Short-term sales designed to trigger impulse purchases."
    },
    {
        "name": "Popularity Claims",
        "category": "Social Proof",
        "regex": re.compile(r"(bestseller|best\s+selling|most\s+popular|top\s+rated|#1\s+(rated|choice|selling)|award[\s-]?winning|highly\s+rated|customer\s+favorite|fan\s+favorite|trending)", re.I),
        "explanation": "Claims popularity to influence purchasing decisions."
    },
    {
        "name": "Activity Notifications",
        "category": "Social Proof",
        "regex": re.compile(r"(\d+\s+people\s+(are\s+)?(viewing|watching|bought)|someone\s+(just\s+)?(bought|purchased|signed\s+up)|recently\s+purchased|in\s+\d+\s+carts|trending\s+now|hot\s+right\s+now)", re.I),
        "explanation": "Shows real-time activity to create social pressure."
    },
    {
        "name": "Testimonial Pressure",
        "category": "Social Proof",
        "regex": re.compile(r"(customers\s+(love|say|rave)|users\s+agree|verified\s+(buyer|purchase|review)|\d+[\d,]*\s*(happy\s+customers|\+?\s*reviews|satisfied\s+users)|join\s+\d+[\d,]*\s*(others|customers|users)|trusted\s+by\s+\d+)", re.I),
        "explanation": "Uses customer testimonials and numbers to build trust."
    },
    {
        "name": "Authority Appeal",
        "category": "Social Proof",
        "regex": re.compile(r"(as\s+seen\s+(on|in)|featured\s+(in|on|by)|endorsed\s+by|recommended\s+by\s+(doctors?|experts?|professionals?)|clinically\s+proven|scientifically\s+proven|backed\s+by\s+science|expert[\s-]?approved)", re.I),
        "explanation": "Leverages authority figures or media mentions for credibility."
    },
    {
        "name": "Anchoring",
        "category": "Pricing Tricks",
        "regex": re.compile(r"(was\s+\$?\d+|originally\s+\$?\d+|compare\s+at\s+\$?\d+|retail\s+(value|price)\s+\$?\d+|save\s+\$?\d+|you\s+save|\d+%\s+off|marked\s+down\s+from)", re.I),
        "explanation": "Shows inflated original prices to make discounts seem larger."
    },
    {
        "name": "Price Anchoring (Under X)",
        "category": "Pricing Tricks",
        "regex": re.compile(r"(under\s+\$?\d+|below\s+\$?\d+|less\s+than\s+\$?\d+|from\s+\$?\d+|starting\s+at\s+\$?\d+|as\s+low\s+as\s+\$?\d+|just\s+\$?\d+)", re.I),
        "explanation": "Frames prices as bargains using anchoring language."
    },
    {
        "name": "Hidden Costs",
        "category": "Pricing Tricks",
        "regex": re.compile(r"(prices?\s+may\s+vary|\+\s*(shipping|tax|fees)|additional\s+fees\s+(may\s+)?apply|terms\s+apply|conditions\s+apply)", re.I),
        "explanation": "Advertises low prices while hiding additional costs."
    },
    {
        "name": "Decoy Pricing",
        "category": "Pricing Tricks",
        "regex": re.compile(r"(best\s+value|most\s+popular\s+plan|recommended\s+plan|save\s+\d+%\s+with\s+(annual|yearly)|billed\s+(annually|yearly)|per\s+month\s+billed\s+annually)", re.I),
        "explanation": "Steers users toward specific pricing tiers using decoys."
    },
    {
        "name": "Deal/Discount Language",
        "category": "Pricing Tricks",
        "regex": re.compile(r"(see\s+all\s+deals|shop\s+deals|new\s+year\s+deals?|holiday\s+deals?|clearance|sale\s+price|special\s+offer|bonus\s+deal|extra\s+savings|double\s+discount)", re.I),
        "explanation": "Uses deal-focused language to trigger bargain-seeking behavior."
    },
    {
        "name": "Email Capture",
        "category": "Data Harvesting",
        "regex": re.compile(r"(enter\s+your\s+email|subscribe\s+(to\s+our|now|today)|join\s+our\s+(newsletter|mailing\s+list)|get\s+updates|stay\s+informed|be\s+the\s+first\s+to\s+know|sign\s+up\s+for\s+(exclusive|early)\s+access)", re.I),
        "explanation": "Prompts users to provide email addresses for marketing."
    },
    {
        "name": "Account Pressure",
        "category": "Data Harvesting",
        "regex": re.compile(r"(create\s+(an?\s+)?account|register\s+now|sign\s+up\s+(today|now|free)|join\s+(today|now|free|us)|get\s+started\s+free|start\s+your\s+free|unlock\s+(access|features))", re.I),
        "explanation": "Pushes account creation to capture user data."
    },
    {
        "name": "Sign In Prompts",
        "category": "Data Harvesting",
        "regex": re.compile(r"(sign\s+in|log\s+in|hello,?\s+sign\s+in|account\s+&\s+lists|my\s+account|your\s+account)", re.I),
        "explanation": "Persistent sign-in prompts to encourage account creation and tracking."
    },
    {
        "name": "Free Bait",
        "category": "Data Harvesting",
        "regex": re.compile(r"(free\s+(trial|download|ebook|guide|sample|consultation|quote|estimate|demo|shipping|delivery|returns?)|get\s+(it\s+)?free|claim\s+your\s+free|download\s+now|instant\s+access|no\s+credit\s+card\s+required)", re.I),
        "explanation": "Offers free items as bait to capture user information."
    },
    {
        "name": "Quiz/Survey Trap",
        "category": "Data Harvesting",
        "regex": re.compile(r"(take\s+(the|our)\s+(quiz|survey|assessment)|find\s+out\s+(which|what|your)|discover\s+your|what's\s+your\s+\w+\s+style|personalized\s+(results|recommendations))", re.I),
        "explanation": "Uses quizzes to collect personal data under the guise of personalization."
    },
    {
        "name": "Prime/Membership Push",
        "category": "Data Harvesting",
        "regex": re.compile(r"(prime\s+(video|member|delivery|free)|join\s+prime|try\s+prime|membership|subscribe\s+&\s+save|loyalty\s+program|rewards?\s+program)", re.I),
        "explanation": "Promotes subscription services to lock users into ecosystem."
    },
    {
        "name": "Fear of Missing Out",
        "category": "FOMO & Emotion",
        "regex": re.compile(r"(don't\s+miss(\s+out)?|missing\s+out|before\s+(it's\s+gone|they're\s+gone)|never\s+miss|you'll\s+regret|once\s+it's\s+gone|won't\s+last|going\s+fast)", re.I),
        "explanation": "Triggers fear of missing out on opportunities."
    },
    {
        "name": "Exclusivity",
        "category": "FOMO & Emotion",
        "regex": re.compile(r"(exclusive\s+(access|offer|deal|discount)|vip\s+(access|members?|only)|members?\s+only|invite[\s-]?only|limited\s+(access|edition|release)|early\s+access|insider|private\s+(sale|access))", re.I),
        "explanation": "Creates artificial exclusivity to make users feel special."
    },
    {
        "name": "Guilt Tripping",
        "category": "FOMO & Emotion",
        "regex": re.compile(r"(no\s+thanks,?\s+i\s+(don't\s+want|hate|prefer)|i('ll)?\s+(stay|remain)\s+(broke|poor|unsuccessful)|i\s+don't\s+(need|want)\s+(success|savings|help)|maybe\s+later|remind\s+me\s+never)", re.I),
        "explanation": "Uses guilt-inducing decline options (confirmshaming)."
    },
    {
        "name": "Loss Aversion",
        "category": "FOMO & Emotion",
        "regex": re.compile(r"(don't\s+lose|you('re|\s+are)\s+(losing|missing)|stop\s+(losing|wasting)|losing\s+out|what\s+you('re|\s+are)\s+missing|cost\s+of\s+(waiting|inaction)|every\s+day\s+(without|you\s+wait))", re.I),
        "explanation": "Frames inaction as a loss rather than a neutral choice."
    },
    {
        "name": "Sensationalism",
        "category": "Clickbait",
        "regex": re.compile(r"(shocking|unbelievable|mind[\s-]?blowing|jaw[\s-]?dropping|incredible|amazing\s+deal|insane\s+(deal|price|savings)|crazy\s+(deal|price)|wild|epic|game[\s-]?changer|revolutionary|breakthrough)", re.I),
        "explanation": "Uses sensational adjectives to exaggerate claims."
    },
    {
        "name": "Curiosity Gap",
        "category": "Clickbait",
        "regex": re.compile(r"(you\s+won't\s+believe|what\s+happens\s+next|the\s+reason\s+why|here's\s+why|the\s+secret\s+(to|of|behind)|the\s+truth\s+about|what\s+they\s+don't\s+tell\s+you|exposed|revealed|the\s+one\s+thing)", re.I),
        "explanation": "Creates curiosity gaps to drive clicks without delivering value."
    },
    {
        "name": "False Promises",
        "category": "Clickbait",
        "regex": re.compile(r"(guaranteed\s+(results|success|income)|make\s+\$?\d+.*?(fast|quick|easy)|get\s+rich|instant\s+(results|success)|overnight\s+(success|results)|lose\s+\d+\s+pounds?\s+(fast|quick)|effortless|no\s+effort\s+required)", re.I),
        "explanation": "Makes unrealistic promises to lure users."
    },
    {
        "name": "Fake Urgency Buttons",
        "category": "Clickbait",
        "regex": re.compile(r"(claim\s+(now|yours)|grab\s+(it|yours)\s+now|get\s+instant\s+access|yes,?\s+i\s+want|give\s+me|send\s+(it\s+)?to\s+me|i'm\s+ready|activate|unlock\s+now)", re.I),
        "explanation": "Uses action-oriented language to pressure immediate clicks."
    },
    {
        "name": "Shop Now CTAs",
        "category": "Clickbait",
        "regex": re.compile(r"(shop\s+now|buy\s+now|order\s+now|add\s+to\s+cart|get\s+yours|shop\s+the\s+(look|sale|collection)|discover\s+more|explore\s+(more|now|all)|see\s+more|learn\s+more)", re.I),
        "explanation": "Aggressive call-to-action buttons designed to drive immediate action."
    },
    {
        "name": "Risk Reversal",
        "category": "Trust Manipulation",
        "regex": re.compile(r"(money[\s-]?back\s+guarantee|risk[\s-]?free|(no|zero)\s+risk|\d+[\s-]?day\s+(guarantee|refund)|full\s+refund|satisfaction\s+guaranteed|try\s+(it\s+)?risk[\s-]?free|cancel\s+anytime|no\s+commitment|no\s+strings\s+attached)", re.I),
        "explanation": "Removes perceived risk to encourage commitment."
    },
    {
        "name": "Fake Scarcity Badges",
        "category": "Trust Manipulation",
        "regex": re.compile(r"(selling\s+out|almost\s+sold\s+out|back\s+in\s+stock|restocked|limited\s+batch|small\s+batch|handmade|handcrafted|artisan|rare\s+find)", re.I),
        "explanation": "Uses badges and labels to imply artificial scarcity."
    },
    {
        "name": "Security Theater",
        "category": "Trust Manipulation",
        "regex": re.compile(r"(secure\s+(checkout|payment|transaction)|ssl\s+(encrypted|secured?)|256[\s-]?bit\s+encryption|bank[\s-]?level\s+security|your\s+(data|info|information)\s+is\s+safe|we\s+(never|don't)\s+(share|sell)\s+your|privacy\s+protected)", re.I),
        "explanation": "Displays security claims to build false trust."
    },
    {
        "name": "Fast Delivery Claims",
        "category": "Trust Manipulation",
        "regex": re.compile(r"(fast\s+(local\s+)?delivery|same[\s-]?day\s+delivery|next[\s-]?day\s+delivery|express\s+shipping|ships\s+(today|tomorrow|fast)|get\s+it\s+(by|tomorrow|fast)|quick\s+shipping|speedy\s+delivery)", re.I),
        "explanation": "Emphasizes delivery speed to encourage impulse purchases."
    },
    {
        "name": "Easy Returns",
        "category": "Trust Manipulation",
        "regex": re.compile(r"(easy\s+returns?|free\s+returns?|hassle[\s-]?free\s+returns?|no[\s-]?questions?[\s-]?asked|simple\s+returns?|return\s+policy|easy\s+exchange)", re.I),
        "explanation": "Highlights return policies to reduce purchase anxiety."
    },
]
