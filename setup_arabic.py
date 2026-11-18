import os
import struct
import array

TRANSLATIONS = {
    # --- BASE & NAVIGATION ---
    "Edrak Properties | Luxury Real Estate": "إدراك العقارية | عقارات فاخرة",
    "Edrak Properties.": "إدراك العقارية.",
    "Home": "الرئيسية",
    "Why Edrak": "لماذا إدراك",
    "Services": "خدماتنا",
    "Projects": "المشاريع",
    "Leases": "الإيجارات",
    "About Us": "من نحن",
    "Contact Us": "تواصل معنا",
    "Elevating the standard of living and investment in Ajman and across the UAE.": "نرتقي بمعايير السكن والاستثمار العقاري في عجمان وجميع أنحاء دولة الإمارات العربية المتحدة.",
    "Quick Links": "روابط سريعة",
    "Our Services": "خدماتنا",
    "Our Projects": "مشاريعنا",
    "Available Leases": "الوحدات المتاحة للإيجار",
    "Contact": "معلومات التواصل",
    "Connect": "تابعنا",
    "All Rights Reserved.": "جميع الحقوق محفوظة.",
    "Rashidiya Building, M5": "بناية الراشدية، طابق ميزانين M5",
    "Rashidiya 2, Ajman UAE": "الراشدية 2، عجمان، الإمارات العربية المتحدة",

    # --- HOME PAGE (index.html) ---
    "Explore the interactive masterplan": "استكشف المخطط التفاعلي الشامل",
    "Invest with": "استثمر بكل",
    "Certainty.": "ثقة ويقين.",
    "Acquire, manage, and scale high-yield property portfolios. A fully integrated platform for investors, landlords, and global capital.": "امتلك، وأدر، ووسّع محافظك العقارية ذات العوائد المرتفعة. منصة متكاملة للمستثمرين والملاك ورؤوس الأموال العالمية.",
    "Explore Portfolio": "استكشف المحفظة العقارية",
    "View Leases": "عرض الإيجارات",
    "Years of Legacy": "عاماً من العراقة",
    "Managed Asset Value": "قيمة الأصول المدارة",
    "Premium Occupancy": "نسبة إشغال متميزة",
    "Global Investors": "مستثمر عالمي",
    "Our Heritage": "إرثنا العريق",
    "Rooted in Traditions.": "جذور راسخة في الأصالة.",
    "Built for the Future.": "مصممة للمستقبل.",
    "Established over half a century ago as a pioneering force in real estate, we have been a cornerstone of the property market in Ajman. We built our reputation on unshakeable trust, unparalleled local market intelligence, and generational relationships.": "تأسست شركتنا قبل أكثر من نصف قرن كقوة رائدة في القطاع العقاري، وشكلت حجر الزاوية في سوق العقارات في عجمان. بنينا سمعتنا على الثقة الراسخة، والخبرة العميقة بالسوق المحلي، والعلاقات الممتدة عبر الأجيال.",
    "Today, we continue that unbroken legacy as Edrak Properties. Expanding our vision across the U.A.E., we combine our historic roots with highly advanced, interactive property management and data-driven investment strategies.": "واليوم، نواصل هذا الإرث المتصل تحت اسم إدراك العقارية. ومع توسع رؤيتنا في كافة أنحاء دولة الإمارات، نجمع بين جذورنا التاريخية العريقة وأحدث أنظمة إدارة العقارات التفاعلية واستراتيجيات الاستثمار المبنية على البيانات.",
    "Dedicated Support": "دعم متواصل",
    "Income Tax in UAE": "ضريبة الدخل في الإمارات",
    "Our Infrastructure": "بنيتنا المؤسسية",
    "Comprehensive Solutions": "حلول عقارية شاملة",
    "Acquisitions & Sales": "الاستحواذ والمبيعات",
    "Acquire premium off-plan assets or sell secondary market properties with maximum valuation through our discreet networks.": "استحوذ على أصول عقارية متميزة على الخارطة أو بع عقارات السوق الثانوي بأعلى تقييم من خلال شبكاتنا الخاصة.",
    "Explore Division": "استكشف القسم",
    "Leasing & Renting": "التأجير وإدارة العقود",
    "Frictionless tenant placement, digital contract generation, and high-quality unit matchmaking.": "تسكين سلس للمستأجرين، وإصدار عقود رقمية، ومطابقة دقيقة للوحدات السكنية والتجارية.",
    "Property Management": "إدارة الممتلكات",
    "Zero-headache operational care. We handle maintenance, rent collection, and tenant relations entirely in-house.": "رعاية تشغيلية متكاملة دون أي عناء. نتولى الصيانة وتحصيل الإيجارات وشؤون المستأجرين بالكامل عبر فرقنا الداخلية.",
    "Yield Advisory": "استشارات العوائد الاستثمارية",
    "Data-driven ROI optimization and portfolio scaling strategies across the U.A.E. real estate sectors.": "تحسين العائد على الاستثمار استناداً إلى البيانات واستراتيجيات توسيع المحافظ العقارية في دولة الإمارات.",
    "Properties for Rent": "عقارات للإيجار",
    "View All Leases": "عرض جميع الإيجارات",
    "Our Portfolio": "محفظتنا العقارية",
    "Featured Developments": "أبرز المشاريع العقارية",
    "Ready to Move": "جاهز للسكن",
    "Off-Plan": "على الخارطة",
    "Commercial": "تجاري",
    "Trusted by Investors": "محل ثقة المستثمرين",
    "Across the U.A.E & Globally": "في دولة الإمارات وحول العالم",
    "Let's Talk Real Estate": "لنتحدث عن استثمارك العقاري",
    "Our advisory team is ready to assist you. We usually reply within minutes.": "فريقنا الاستشاري مستعد لمساعدتك. نرد عادةً خلال دقائق.",
    "Full Name": "الاسم الكامل",
    "Phone Number": "رقم الهاتف",
    "Email Address": "البريد الإلكتروني",
    "How can we assist you?": "كيف يمكننا مساعدتك؟",
    "Submit Inquiry": "إرسال الاستفسار",
    "Edrak Properties is a premier real estate development and property management firm headquartered in Ajman, United Arab Emirates. With a legacy spanning over 50 years—originally established as Yousuf Bin Nasser & Sons—we have solidified our reputation as the region's most trusted authority in property investment, commercial leasing, and high-yield real estate acquisitions. Our extensive portfolio includes luxury villas, premium off-plan developments, and commercial hubs strategically located across the UAE's most lucrative investment zones.": "إدراك العقارية هي شركة رائدة في التطوير العقاري وإدارة الممتلكات يقع مقرها الرئيسي في عجمان، الإمارات العربية المتحدة. بفضل إرث يمتد لأكثر من 50 عاماً — تأسست في الأصل باسم يوسف بن ناصر وأولاده للعقارات — رسخنا مكانتنا كأكثر جهة موثوقة في المنطقة في الاستثمار العقاري والتأجير التجاري والاستحواذات العقارية ذات العوائد المرتفعة.",
    "Whether you are a global investor seeking tax-free capital appreciation, a business owner requiring prime commercial frontage in the Industrial Freezone, or a family looking for a luxury residence in Al Yasmeen or Downtown Ajman, Edrak Properties delivers comprehensive, data-driven solutions. Our in-house property management division ensures frictionless tenant placement, rigorous maintenance protocols, and maximized ROI, setting the gold standard for real estate infrastructure in the Emirates.": "سواء كنت مستثمراً عالمياً تبحث عن نمو رأسمالي معفى من الضرائب، أو صاحب عمل يحتاج إلى واجهة تجارية متميزة في المنطقة الحرة الصناعية، أو عائلة تبحث عن مسكن فاخر في الياسمين أو وسط مدينة عجمان، تقدم إدراك العقارية حلولاً شاملة ومبنية على البيانات تضمن أعلى عائد استثماري.",

    # --- SERVICES PAGE (services.html) ---
    "Our Divisions": "أقسامنا المتخصصة",
    "Comprehensive": "حلول عقارية",
    "Solutions.": "متكاملة.",
    "From off-plan acquisitions to elite property management, Edrak provides end-to-end infrastructure for the modern real estate investor across all asset classes.": "من الاستحواذ على المشاريع على الخارطة إلى الإدارة الاحترافية للممتلكات، توفر إدراك بنية تحتية متكاملة للمستثمر العقاري العصري عبر كافة فئات الأصول.",
    "Tailored Expertise": "خبرات مصممة خصيصاً",
    "Excellence Across Every Pillar & Asset Class": "التميز عبر كل ركيزة وفئة أصول عقارية",
    "Leverage localized data in the Ajman and wider U.A.E. market to price, list, and sell with precision. Access exclusive off-plan developments and high-yield secondary market assets.": "استفد من البيانات الدقيقة في سوق عجمان والإمارات لتسعير وإدراج وبيع العقارات بدقة عالية، والوصول إلى مشاريع حصرية على الخارطة وأصول عالية العائد.",
    "Off-Plan Investments": "استثمارات المشاريع على الخارطة",
    "Secondary Market Sales": "مبيعات السوق الثانوي",
    "Accurate Portfolio Valuation": "تقييم دقيق للمحافظ العقارية",
    "Consult an Agent": "استشر مستشاراً عقارياً",
    "Eliminating the friction of property leasing. Matching premium tenants with luxury residential and commercial assets with rigorous background screening and digital contracts.": "القضاء على صعوبات التأجير العقاري من خلال ربط المستأجرين المتميزين بالأصول السكنية والتجارية الفاخرة مع فحص دقيق وإدارة عقود رقمية.",
    "Residential Matchmaking": "تسكين الوحدات السكنية",
    "Commercial Leasing": "التأجير التجاري",
    "Digital Contract Management": "إدارة العقود الرقمية",
    "View Available Leases": "عرض الوحدات المتاحة للإيجار",
    "A-Z property management ensuring absentee landlords and international investors generate passive income with zero headache, from maintenance to timely rent collection.": "إدارة شاملة للممتلكات من الألف إلى الياء تضمن للملاك والمستثمرين الدوليين تحقيق دخل مستدام دون أي عناء، من الصيانة الدورية إلى تحصيل الإيجارات في موعدها.",
    "Automated Rent Collection": "تحصيل الإيجارات المؤتمت",
    "24/7 Facility Maintenance": "صيانة المرافق على مدار الساعة",
    "Tenant Dispute Resolution": "تسوية منازعات المستأجرين",
    "Assign Your Property": "أوكِل إدارة عقارك إلينا",
    "Data-driven ROI optimization and portfolio scaling strategies. Intelligence needed to maximize capital appreciation across residential and commercial holdings.": "تحسين العائد على الاستثمار وتوسيع المحافظ العقارية استناداً إلى البيانات، وتوفير الرؤى اللازمة لتعظيم النمو الرأسمالي للأصول السكنية والتجارية.",
    "Market Trend Analysis": "تحليل اتجاهات السوق",
    "Portfolio Scaling Strategy": "استراتيجية توسيع المحفظة",
    "ROI Optimization": "تعظيم العائد الاستثماري",
    "Book a Strategy Call": "احجز استشارة استراتيجية",
    "Residential & Villa Estates": "الفلل والمجمعات السكنية",
    "Specialized brokerage and lifestyle curation for luxury private villas, gated community townhouses, and high-end residential apartment complexes across the Emirates.": "وساطة عقارية متخصصة للفلل الخاصة الفاخرة، ومنازل التاون هاوس في المجمعات المسورة، والمجمعات السكنية الراقية في جميع أنحاء الإمارات.",
    "Luxury Villas & Mansions": "الفلل والقصور الفاخرة",
    "Gated Community Townhouses": "تاون هاوس المجمعات المسورة",
    "Residential Apartments": "الشقق السكنية",
    "Explore Residences": "استكشف الوحدات السكنية",
    "Buildings & Warehouses": "المباني والمستودعات الصناعية",
    "Industrial and commercial asset advisory covering entire commercial buildings, logistics warehouses, freezone facilities, and multi-story corporate properties.": "استشارات الأصول الصناعية والتجارية التي تغطي المباني التجارية الكاملة والمستودعات اللوجستية ومرافق المناطق الحرة والعقارات متعددة الطوابق.",
    "Commercial Buildings & Towers": "المباني والأبراج التجارية",
    "Industrial & Storage Warehouses": "المستودعات الصناعية والتخزينية",
    "Retail & Freezone Plots": "محلات التجزئة وأراضي المناطق الحرة",
    "Explore Commercial Assets": "استكشف الأصول التجارية",
    "The Edrak Standard": "معيار إدراك",
    "Shaping Landscapes Across the UAE": "نصوغ المشهد العمراني في دولة الإمارات",
    "Exclusive Portfolio": "محفظة حصرية",
    "Architectural Mastery in Prime Locations": "إتقان معماري في مواقع استراتيجية",
    "Client Success": "نجاح العملاء",
    "Unmatched Yields & Asset Protection": "عوائد استثنائية وحماية متكاملة للأصول",

    # --- ABOUT US PAGE (about.html) ---
    "A Legacy of Trust.": "إرث من الثقة.",
    "Built for Generations.": "بُني للأجيال.",
    "Over 50 Years of Excellence": "أكثر من 50 عاماً من التميز",
    "Edrak Properties stands as a paragon of real estate excellence in Ajman and the wider United Arab Emirates, commanding a portfolio built on half a century of market mastery.": "تقف إدراك العقارية كنموذج للتميز العقاري في عجمان ودولة الإمارات العربية المتحدة، حيث تدير محفظة عقارية راسخة بُنيت على مدى نصف قرن من الريادة في السوق.",
    "Previously known as the highly esteemed Yousuf Bin Nasser & Sons Real Estate, we established the bedrock of the property market in Ajman over fifty years ago. Our foundational years were defined by pioneering developments, unshakeable trust, and the cultivation of generational relationships. To meet the rigorous demands of a globalized economy, we have evolved and rebranded as Edrak Properties—a name that reflects our forward-thinking ethos while remaining deeply anchored in the traditional values that brought us decades of success.": "عُرفت شركتنا سابقاً باسم يوسف بن ناصر وأولاده للعقارات، حيث أرسينا دعائم السوق العقاري في عجمان قبل أكثر من خمسين عاماً. تميزت سنوات التأسيس بالمشاريع الرائدة والثقة الراسخة وبناء العلاقات الممتدة عبر الأجيال. ولمواكبة متطلبات الاقتصاد العالمي الحديث، تطورنا إلى هوية إدراك العقارية — وهو اسم يعكس رؤيتنا المستقبلية مع التمسك العميق بالقيم الأصيلة التي صنعت نجاحنا لعقود.",
    "Today, we have successfully bridged our legacy of market dominance with cutting-edge property management, data-driven yield optimization, and modern digital infrastructure. Our dedicated team of investment advisors, legal experts, and facility managers work relentlessly to elevate the standard of living and investment across the Emirates.": "واليوم، نجحنا في المزج بين إرثنا العريق وأحدث تقنيات إدارة الممتلكات، وتحسين العوائد بالبيانات، والبنية التحتية الرقمية الحديثة. يعمل فريقنا المتخصص من مستشاري الاستثمار والخبراء القانونيين ومديري المرافق بلا كلل للارتقاء بمعايير المعيشة والاستثمار في كافة أنحاء الإمارات.",
    "Whether you are a local family seeking a forever home, a corporate entity acquiring commercial hubs in the Industrial Freezone, or an international investor pursuing high-yield capital appreciation in the tax-free haven of the U.A.E., Edrak Properties provides the end-to-end operational framework required to secure and scale your wealth.": "سواء كنت عائلة تبحث عن منزل العمر، أو مؤسسة تستحوذ على مقرات تجارية في المنطقة الحرة الصناعية، أو مستثمراً دولياً يسعى لتنمية رأس ماله بعوائد مرتفعة في بيئة الإمارات المعفاة من الضرائب، توفر لك إدراك العقارية المنظومة التشغيلية المتكاملة لحماية وتنمية ثروتك.",
    "Our Mission": "رسالتنا",
    "To engineer unparalleled real estate infrastructure that empowers investors, nurtures communities, and redefines the standard of luxury living across the UAE. We meticulously manage, develop, and acquire properties that yield sustainable, long-term capital appreciation, ensuring every asset under our stewardship operates at absolute peak efficiency.": "هندسة بنية تحتية عقارية لا مثيل لها تمكّن المستثمرين، وتثري المجتمعات، وتعيد تعريف معايير الحياة الفاخرة في الإمارات. نحن ندير ونطور ونستحوذ بعناية فائقة على العقارات التي تحقق نمواً رأسمالياً مستداماً طويل الأمد، مع ضمان تشغيل كل أصل تحت إشرافنا بأقصى درجات الكفاءة.",
    "Our Vision": "رؤيتنا",
    "To be the premier architectural and property management institution in the Middle East. We envision a landscape where traditional values of trust and transparency seamlessly integrate with cutting-edge prop-tech and data-driven yield advisory, making Edrak the ultimate conduit for global capital entering the UAE real estate sector.": "أن نكون المؤسسة الرائدة في التطوير وإدارة العقارات في الشرق الأوسط. نتطلع إلى مستقبل تتكامل فيه قيم الثقة والشفافية الأصيلة مع أحدث التقنيات العقارية واستشارات العوائد المبنية على البيانات، لتكون إدراك البوابة الأولى لرؤوس الأموال العالمية في قطاع العقارات الإماراتي.",
    "A Dedicated Infrastructure": "بنية مؤسسية متكاملة",
    "Operational Excellence at Every Level": "التميز التشغيلي على كافة المستويات",
    "Market Intelligence": "ذكاء السوق العقاري",
    "Leveraging 50 years of proprietary data to identify high-yield investment zones and execute flawless acquisitions.": "الاستفادة من 50 عاماً من البيانات العقارية لتحديد مناطق الاستثمار ذات العوائد المرتفعة وتنفيذ عمليات استحواذ ناجحة.",
    "Dedicated Team": "فريق متخصص",
    "An elite, in-house team of sales directors, legal consultants, and facility managers providing 24/7 operational care.": "نخبة من مديري المبيعات والمستشارين القانونيين ومديري المرافق الداخليين لتقديم رعاية تشغيلية على مدار الساعة.",
    "Asset Maximization": "تعظيم قيمة الأصول",
    "Strategic rent pricing models, minimal vacancy rates, and stringent tenant matchmaking to ensure premium ROI.": "نماذج تسعير إيجارية استراتيجية، وأدنى معدلات شغور، واختيار دقيق للمستأجرين لضمان أعلى عائد على الاستثمار.",
    "Global Capital": "رأس المال العالمي",
    "Facilitating seamless property acquisitions for international investors looking to scale portfolios in the tax-free U.A.E.": "تسهيل عمليات الاستحواذ العقاري السلسة للمستثمرين الدوليين الراغبين في توسيع محافظهم في دولة الإمارات المعفاة من الضرائب.",
    "A Glimpse of Our Portfolio": "لمحة عن محفظتنا العقارية",
    "Captured Across Our Developments": "لقطات من مشاريعنا ومبانينا",
    "View All Projects": "عرض جميع المشاريع",
    "View Project": "عرض المشروع",
    "Our Headquarters": "مقرنا الرئيسي",
    "Ajman, United Arab Emirates": "عجمان، الإمارات العربية المتحدة",

    # --- PROJECTS, LEASES & DETAILS ---
    "Our Developments": "مشاريعنا العقارية",
    "Master Projects": "المشاريع الرئيسية",
    "Explore our portfolio of elite developments. Click on any project to view exclusively available leases within that building.": "استكشف محفظتنا من المشاريع العقارية النخبة. اضغط على أي مشروع لعرض الوحدات المتاحة للإيجار داخل المبنى.",
    "View Project Details": "عرض تفاصيل المشروع",
    "No projects available currently.": "لا توجد مشاريع متاحة حالياً.",
    "Back to Projects": "العودة إلى المشاريع",
    "Description": "الوصف التفصيلي",
    "Features & Amenities": "المميزات والمرافق",
    "Total Units": "إجمالي الوحدات",
    "Parking Available": "مواقف سيارات متوفرة",
    "No Parking": "لا تتوفر مواقف",
    "Inquire Now": "استفسر الآن",
    "Contact Advisor": "تواصل مع المستشار",
    "Location": "الموقع",
    "All Locations": "جميع المواقع",
    "Project/Building": "المشروع / المبنى",
    "All Projects": "جميع المشاريع",
    "Min Beds": "الحد الأدنى للغرف",
    "Any": "الكل",
    "Max Rent (AED)": "الحد الأقصى للإيجار (درهم)",
    "Filter Results": "تصفية النتائج",
    "Details": "التفاصيل",
    "Call": "اتصال",
    "WhatsApp": "واتساب",
    "No properties match your exact criteria.": "لا توجد عقارات تطابق معايير البحث الخاصة بك.",
    "Clear Filters": "مسح التصفية",
    "Back to Leases": "العودة إلى الإيجارات",
    "Annual Rent": "الإيجار السنوي",
    "Bedrooms": "غرف النوم",
    "Bathrooms": "الحمامات",
    "Size": "المساحة",
    "Parking": "مواقف السيارات",
    "Property Features": "مميزات العقار",
    "Standard features included.": "المميزات القياسية متضمنة.",
    "Contact Agent": "تواصل مع الوكيل",
    "Call Now": "اتصل الآن",
    "Get in Touch": "تواصل معنا",
    "Speak to an Advisor": "تحدث إلى مستشار عقاري",
    "Head Office": "المكتب الرئيسي",

    # --- WHY EDRAK PAGE (why_edrak.html) ---
    "Institutional Dossier": "الملف المؤسسي",
    "The YBN Pedigree": "إرث يوسف بن ناصر",
    "Track Record": "سجل الإنجازات",
    "50-Year Timeline": "مسيرة 50 عاماً",
    "Our Buildings": "مبانينا",
    "Featured Units": "الوحدات المميزة",
    "Yield Simulator": "حاسبة العوائد",
    "Operations": "المنظومة التشغيلية",
    "Client Trust": "ثقة العملاء",
    "Partner With Us": "شاركنا النجاح",
    "Formerly Yousuf Bin Nasser & Sons Real Estate • Est. Over 50 Years": "سابقاً يوسف بن ناصر وأولاده للعقارات • تأسست منذ أكثر من 50 عاماً",
    "Half a Century of": "نصف قرن من",
    "Unshakeable Trust.": "الثقة الراسخة.",
    "In a market crowded with transient brokerages, Edrak Properties stands apart as a generational institution. Born from the half-century legacy of Yousuf Bin Nasser & Sons Real Estate, we do not merely transact property—we engineer, own, manage, and protect enduring real estate wealth across Ajman and the United Arab Emirates.": "في سوق يزخر بشركات الوساطة المؤقتة، تنفرد إدراك العقارية كمؤسسة عريقة تمتد عبر الأجيال. انطلاقاً من إرث يوسف بن ناصر وأولاده للعقارات الممتد لنصف قرن، نحن لا نكتفي بصفقات البيع والشراء فحسب — بل نبني ونمتلك وندير ونحمي الثروات العقارية المستدامة في عجمان ودولة الإمارات العربية المتحدة.",
    "Inspect Our Building Portfolio": "تصفح محفظة مبانينا",
    "Explore Our 50-Year Pedigree": "استكشف إرثنا الممتد لـ 50 عاماً",
    "Foundation & Heritage": "التأسيس والإرث",
    "Yousuf Bin Nasser & Sons Real Estate": "يوسف بن ناصر وأولاده للعقارات",
    "Executive Leadership": "القيادة التنفيذية",
    "Mr. Mohammed Yousef Nasser Al Nuaimi": "السيد محمد يوسف ناصر النعيمي",
    "Corporate Headquarters": "المقر الرئيسي للشركة",
    "Rashidiya Building, M5, Ajman, UAE": "بناية الراشدية، M5، عجمان، الإمارات",
    "Operational Standard": "المعيار التشغيلي",
    "Principal Asset Owner & 360° Operator": "مالك رئيسي للأصول ومشغل متكامل 360°",
    "Institutional Continuity": "الاستمرارية المؤسسية",
    "From Yousuf Bin Nasser & Sons to Edrak Properties: One Unbroken Promise.": "من يوسف بن ناصر وأولاده إلى إدراك العقارية: عهد واحد لا ينقطع.",
    "Years in UAE": "عاماً في الإمارات",
    "Built on decades of tangible brick-and-mortar ownership across Ajman, protecting multi-generational family capital and international institutional portfolios alike.": "بُنيت على عقود من الملكية العقارية الفعلية في كافة أنحاء عجمان، لحماية رؤوس الأموال العائلية الممتدة عبر الأجيال والمحافظ المؤسسية الدولية على حد سواء.",
    "The Pedigree & Bloodline": "الأصالة والجذور العريقة",
    "Roots Cast in Stone.": "جذور راسخة في الصخر.",
    "Vision Built for Tomorrow.": "ورؤية مشيدة للمستقبل.",
    "To understand why discerning landlords, sovereign-tier investors, and thousands of families trust Edrak Properties, one must look at our foundation: Yousuf Bin Nasser & Sons Real Estate (YBN). For over fifty years, the Yousuf Bin Nasser name has been synonymous with reliability, ethical stewardship, and urban pioneering in Ajman and across the Emirates.": "لفهم السبب الذي يجعل كبار الملاك والمستثمرين وآلاف العائلات يثقون في إدراك العقارية، يجب النظر إلى أساسنا المتين: شركة يوسف بن ناصر وأولاده للعقارات. على مدى أكثر من خمسين عاماً، ارتبط اسم يوسف بن ناصر بالمصداقية والأمانة والريادة العمرانية في عجمان ودولة الإمارات.",
    "Long before modern glass towers defined the skyline, Yousuf Bin Nasser & Sons Real Estate was acquiring strategic land, constructing enduring residential and commercial buildings, and establishing a reputation where a handshake carried the weight of an ironclad contract.": "قبل وقت طويل من ظهور الأبراج الزجاجية الحديثة، كانت شركة يوسف بن ناصر وأولاده للعقارات تستحوذ على الأراضي الاستراتيجية، وتشيد المباني السكنية والتجارية الراسخة، وتبني سمعةً كانت فيها المصافحة تعادل قوة العقد الموثق.",
    "Under the visionary leadership of CEO Mr. Mohammed Yousef Nasser Al Nuaimi, the company evolved into Edrak Properties—meaning 'Perception, Deep Understanding, and Realization.' This evolution united half a century of physical asset ownership with modern data analytics, automated financial transparency, and institutional-grade facility management.": "وتحت القيادة الرشيدة للرئيس التنفيذي السيد محمد يوسف ناصر النعيمي، تطورت الشركة إلى إدراك العقارية — وهو اسم يجسد الفهم العميق والإدراك المستقبلي. وحّد هذا التطور نصف قرن من ملكية الأصول العقارية مع التحليلات الحديثة للبيانات والشفافية المالية المؤتمتة وإدارة المرافق بمعايير مؤسسية عالمية.",
    "Our name changed to reflect our technological and analytical evolution, but our soul remains the exact legacy of Yousuf Bin Nasser & Sons. Every building we manage is maintained as if our own family name is etched onto its facade—because for over fifty years, it has been.": "لقد تغير اسمنا ليعكس تطورنا التقني والتحليلي، لكن جوهرنا يظل هو ذاته إرث يوسف بن ناصر وأولاده. كل مبنى نديره تتم صيانته ورعايته وكأن اسم عائلتنا محفور على واجهته — لأنه على مدى أكثر من خمسين عاماً، كان كذلك بالفعل.",
    "Chief Executive Officer • Edrak Properties": "الرئيس التنفيذي • إدراك العقارية",
    "Quantified Dependability": "موثوقية مثبتة بالأرقام",
    "A Track Record Audited by Time": "سجل حافل يشهده الزمن",
    "Real estate claims are easy to make; five decades of uninterrupted occupancy, asset appreciation, and on-time landlord disbursements are impossible to fabricate.": "من السهل إطلاق الوعود العقارية؛ لكن خمسة عقود من الإشغال المتواصل ونمو قيمة الأصول وتحويل عوائد الملاك في مواعيدها هي حقائق لا يمكن تصنعها.",
    "Market Longevity": "العراقة في السوق",
    "Years": "عاماً",
    "Continuous real estate operations in Ajman and the UAE, weathering every global economic cycle with zero defaults.": "عمليات عقارية متواصلة في عجمان والإمارات، صمدت أمام كافة الدورات الاقتصادية العالمية بسجل خالٍ من أي تعثر.",
    "Portfolio Valuation": "تقييم المحفظة العقارية",
    "In active residential towers, commercial buildings, luxury villas, and industrial assets under direct Edrak stewardship.": "في الأبراج السكنية النشطة والمباني التجارية والفلل الفاخرة والأصول الصناعية تحت الإدارة المباشرة لشركة إدراك.",
    "Asset Demand": "الطلب على الأصول",
    "Sustained occupancy rate across our managed buildings, driven by proactive maintenance and tenant-first governance.": "معدل إشغال مستدام عبر مبانينا المدارة، مدفوعاً بالصيانة الاستباقية والحوكمة التي تضع راحة المستأجر في المقام الأول.",
    "Community & Network": "المجتمع والشبكة الاستثمارية",
    "Global investors, commercial enterprises, and residential families served across our buildings and advisory mandates.": "من المستثمرين العالميين والشركات التجارية والعائلات السكنية الذين تشرفنا بخدمتهم عبر مبانينا واستشاراتنا.",
    "Engineering Response": "الاستجابة الهندسية",
    "In-House SLA": "فريق صيانة داخلي",
    "Dedicated technical maintenance crews, HVAC specialists, and audited rapid-response dispatchers protecting every unit.": "فرق صيانة فنية متخصصة، وخبراء تكييف وتبريد، ومنسقو استجابة سريعة لحماية كل وحدة عقارية.",
    "Tenant Retention": "الاحتفاظ بالمستأجرين",
    "Multi-year lease renewal rate, eliminating costly turnover vacancies and stabilizing net cash flow for property owners.": "معدل تجديد عقود الإيجار لعدة سنوات، مما يقضي على فترات الشغور المكلفة ويضمن استقرار التدفق النقدي الصافي للملاك.",
    "Chronicle of Excellence": "سجل التميز عبر العقود",
    "Five Decades of Shaping the Emirates": "خمسة عقود من البناء والتطوير في الإمارات",
    "Select an era below to explore how Yousuf Bin Nasser & Sons Real Estate grew from a pioneering local land steward into Edrak Properties.": "اختر حقبة زمنية أدناه لاستكشاف كيف نمت شركة يوسف بن ناصر وأولاده للعقارات من رائد محلي إلى مؤسسة إدراك العقارية.",
    "The Founding": "التأسيس",
    "Urban Expansion": "التوسع العمراني",
    "Tower Landmarks": "الأبراج المعالم",
    "Edrak Rebrand": "الانطلاقة الجديدة",
    "PropTech & Scale": "التقنية والتوسع",
    "Genesis of a Dynasty": "بداية مسيرة عريقة",
    "1970s • Genesis of a Dynasty": "السبعينيات • بداية مسيرة عريقة",
    "1980s – 1990s • Building the Urban Core": "الثمانينيات والتسعينيات • بناء النواة العمرانية",
    "2000s – 2010s • Institutional Asset Scale": "الألفية الجديدة • التوسع المؤسسي للأصول",
    "2020 – 2024 • The Evolution into Edrak Properties": "2020 – 2024 • التطور إلى إدراك العقارية",
    "2025 – Future • Next-Generation PropTech & Scale": "2025 – المستقبل • الجيل القادم من التقنية العقارية",
    "Establishment of Yousuf Bin Nasser & Sons Real Estate": "تأسيس شركة يوسف بن ناصر وأولاده للعقارات",
    "As the United Arab Emirates forged its historic union, Yousuf Bin Nasser & Sons Real Estate established its foundational footprint in Ajman. Focusing on essential housing, merchant commercial spaces, and long-term land banking, the firm earned an immediate reputation among founding families for absolute integrity and fair dealing.": "مع قيام اتحاد دولة الإمارات العربية المتحدة، أرست شركة يوسف بن ناصر وأولاده للعقارات بصمتها التأسيسية في إمارة عجمان. ومن خلال التركيز على المساكن الأساسية والمساحات التجارية وتطوير الأراضي، اكتسبت الشركة سمعة فورية بين العائلات المؤسسة للنزاهة المطلقة والتعامل العادل.",
    "Shaping Ajman's Residential & Commercial Corridors": "تشكيل المحاور السكنية والتجارية في عجمان",
    "Throughout the 1980s and 1990s, Yousuf Bin Nasser & Sons scaled rapidly alongside Ajman's demographic boom. The firm developed multi-family residential buildings and retail streetfronts across Al Rashidiya and central districts, becoming a trusted custodian for local landlords and regional merchant families.": "خلال الثمانينيات والتسعينيات، توسعت شركة يوسف بن ناصر وأولاده بسرعة مواكبةً للنهضة العمرانية في عجمان. طورت الشركة مباني سكنية ومحلات تجارية في الراشدية والمناطق المركزية، لتصبح الأمين الموثوق للملاك المحليين وعائلات التجار في المنطقة.",
    "Flagship Multi-Story Towers, Villas & Industrial Hubs": "الأبراج متعددة الطوابق والفلل والمراكز الصناعية",
    "Entering the new millennium, the portfolio expanded into landmark multi-story buildings and commercial anchors across Ajman, alongside private luxury villas and strategic estates.": "مع دخول الألفية الجديدة، توسعت المحفظة لتشمل مباني بارزة متعددة الطوابق ومراكز تجارية في أنحاء عجمان، إلى جانب الفلل الفاخرة الخاصة والعقارات الاستراتيجية.",
    "Modernizing a 50-Year Legacy Under Mr. Mohammed Al Nuaimi": "تحديث إرث يمتد لـ 50 عاماً بقيادة السيد محمد النعيمي",
    "Led by CEO Mr. Mohammed Yousef Nasser Al Nuaimi, Yousuf Bin Nasser & Sons Real Estate strategically transformed into Edrak Properties. The rebrand united 50+ years of family pedigree with modern institutional governance, digital contract workflows, and data-backed yield advisory.": "بقيادة الرئيس التنفيذي السيد محمد يوسف ناصر النعيمي، تحولت شركة يوسف بن ناصر وأولاده للعقارات استراتيجياً إلى إدراك العقارية. وحدت هذه الهوية أكثر من 50 عاماً من العراقة العائلية مع الحوكمة المؤسسية الحديثة وإدارة العقود الرقمية واستشارات العوائد المبنية على البيانات.",
    "AI-Audited Maintenance, 99.9% Occupancy & Regional Growth": "صيانة مدققة بالذكاء الاصطناعي وإشغال 99.9% ونمو إقليمي",
    "Today, Edrak Properties operates at the intersection of timeless hospitality and modern engineering—deploying automated invoice auditing, GPS-tracked 24/7 maintenance crews, and real-time financial synchronization to set the gold standard for real estate across the UAE.": "اليوم، تعمل إدراك العقارية عند نقطة الالتقاء بين الأصالة والهندسة الحديثة — عبر نشر التدقيق الآلي للفواتير، وفرق الصيانة المتتبعة عبر نظام تحديد المواقع على مدار الساعة، والمزامنة المالية الفورية لإرساء المعيار الذهبي للعقارات في الإمارات.",
    "Key Milestone": "أبرز إنجاز مرحلي",
    "First Commercial & Residential Plots in Central Ajman": "أولى الأراضي والمباني التجارية والسكنية في وسط عجمان",
    "Expansion Across Al Rashidiya & Central Districts": "التوسع عبر منطقة الراشدية والمناطق المركزية",
    "Over AED 1 Billion in Managed & Owned Assets": "أكثر من مليار درهم من الأصول المملوكة والمدارة",
    "Launch of Edrak Corporate Identity & HQ at Rashidiya M5": "إطلاق الهوية المؤسسية لإدراك والمقر الرئيسي في بناية الراشدية M5",
    "99.9% Portfolio Occupancy & 10,000+ Network Milestone": "نسبة إشغال 99.9% وشبكة تضم أكثر من 10,000 عميل ومستثمر",
    "Core Pillar Established": "الركيزة الأساسية",
    "Generational Handshake Trust & Land Stewardship": "ثقة الأجيال الراسخة وإدارة الأراضي الاستراتيجية",
    "Long-Term Tenant Retention & Community Building": "الاحتفاظ بالمستأجرين على المدى الطويل وبناء المجتمعات",
    "In-House Engineering & Full-Lifecycle Custody": "الهندسة الداخلية والرعاية المتكاملة لدورة حياة العقار",
    "Data-Driven Yield Optimization & Global Investor Access": "تعظيم العوائد بالبيانات وتمكين المستثمرين العالميين",
    "Predictive Asset Protection & Generational Wealth": "الحماية الاستباقية للأصول وتنمية ثروات الأجيال",
    "Foundational UAE Urban Growth": "النهضة العمرانية التأسيسية في الإمارات",
    "Expanding Commercial & Residential Corridors": "توسيع المحاور التجارية والسكنية",
    "Multi-Story Landmark Portfolio": "محفظة المباني والأبراج متعددة الطوابق",
    "The Edrak Institutional Era": "عصر إدراك المؤسسي",
    "Future-Ready Real Estate Infrastructure": "بنية تحتية عقارية جاهزة للمستقبل",
    "The Definitive Distinction": "الفرق الجوهري",
    "Why Choose Edrak Over Any Other Firm?": "لماذا تختار إدراك العقارية دون غيرها؟",
    "Most real estate agencies only care until the commission cheque clears. Because Edrak Properties was born as an asset-owning family enterprise (Yousuf Bin Nasser & Sons), our entire operational DNA is built to protect property value over decades, not days.": "تهتم معظم وكالات العقارات فقط حتى لحظة صرف شيك العمولة. ولأن إدراك العقارية وُلدت كمؤسسة عائلية مالكة للأصول (يوسف بن ناصر وأولاده)، فإن منظومتنا التشغيلية بالكامل مصممة لحماية قيمة العقار عبر العقود وليس لأيام معدودة.",
    "Skin in the Game": "شركاء في الملكية",
    "Principal Owner Mentality": "عقلية المالك الرئيسي",
    "We own and operate our own flagship buildings alongside client portfolios. We never experiment with your capital—we apply the exact maintenance, leasing, and legal protocols that safeguard our own family estates.": "نحن نمتلك وندير مبانينا الرئيسية الخاصة جنباً إلى جنب مع محافظ عملائنا. لا نجازف أبداً برأس مالك — بل نطبق ذات بروتوكولات الصيانة والتأجير والشؤون القانونية التي تحمي ممتلكات عائلتنا.",
    "Zero Subcontracting Lag": "دون وسطاء صيانة",
    "In-House Technical & Maintenance Fleet": "أسطول فني وهندسي داخلي للصيانة",
    "Deferred maintenance silently destroys property yields. Edrak commands an audited, GPS-tracked 24/7 engineering and facility crew—handling HVAC, plumbing, electrical, and civil works at wholesale material cost.": "الصيانة المؤجلة تستنزف عوائد العقارات بصمت. تقود إدراك فريقاً هندسياً وفنياً داخلياً يعمل على مدار الساعة — يتولى أعمال التكييف والسباكة والكهرباء والأعمال المدنية بتكلفة المواد الأساسية.",
    "Financial Precision": "دقة مالية متناهية",
    "Institutional Accounting & PDC Custody": "محاسبة مؤسسية وإدارة دقيقة للشيكات المؤجلة",
    "Every dirham is tracked through synchronized enterprise ledgers. From post-dated cheque (PDC) clearing and automated rent reminders to itemized maintenance invoicing, landlords enjoy 100% audit-ready clarity.": "يتم تتبع كل درهم عبر دفاتر محاسبية مؤسسية متزامنة. من تحصيل الشيكات المؤجلة والتذكير الآلي بالإيجارات إلى فواتير الصيانة المفصلة، يتمتع الملاك بشفافية مالية جاهزة للتدقيق بنسبة 100%.",
    "Quality Occupancy": "جودة الإشغال",
    "Rigorous 4-Point Tenant Vetting": "فحص دقيق للمستأجرين من 4 مراحل",
    "High occupancy means nothing if tenants default. We verify employment, corporate trade licenses, banking history, and prior tenancy records—resulting in a 99.9% occupancy rate and minimal legal disputes.": "لا قيمة للإشغال المرتفع إذا تعثر المستأجرون. نحن نتحقق من جهات العمل والرخص التجارية والسجل المصرفي وسوابق الإيجار — مما يثمر عن نسبة إشغال 99.9% وأدنى حد من النزاعات القانونية.",
    "Market Authority": "الريادة في السوق",
    "Unrivaled Ajman & Northern Emirates Access": "وصول لا يضاهى في عجمان والإمارات الشمالية",
    "Five decades as Yousuf Bin Nasser & Sons gives us direct access to off-market land plots, high-yield whole buildings, and municipal regulatory speed that newcomers simply cannot replicate.": "خمسة عقود تحت اسم يوسف بن ناصر وأولاده تمنحنا وصولاً مباشراً إلى الأراضي الحصرية والمباني الكاملة عالية العائد وسرعة الإجراءات التنظيمية والبلدية التي لا يمكن للشركات الجديدة مضاهاتها.",
    "Absentee Peace of Mind": "راحة بال تامة للملاك",
    "Turnkey Global Investor Custody": "إدارة متكاملة للمستثمرين حول العالم",
    "Whether you reside in Ajman, Dubai, London, or Riyadh, Edrak acts as your single point of accountability—handling municipal attestations, Tasdeeq contracts, utilities, and net yield transfers seamlessly.": "سواء كنت مقيماً في عجمان أو دبي أو لندن أو الرياض، تعمل إدراك كجهة مسؤولة واحدة تنوب عنك — حيث تتولى تصديق العقود والبلدية والمرافق وتحويل صافي العوائد بكل سلاسة.",
    "Side-By-Side Benchmark": "مقارنة معيارية مباشرة",
    "The Edrak Standard vs. Conventional Agencies": "معيار إدراك مقابل وكالات العقارات التقليدية",
    "Backed by 50+ Years of YBN Institutional Heritage": "مدعومة بأكثر من 50 عاماً من الإرث المؤسسي ليوسف بن ناصر",
    "Core Capability": "القدرة الأساسية",
    "Edrak Properties (YBN Legacy)": "إدراك العقارية (إرث يوسف بن ناصر)",
    "Typical Market Brokerage": "شركة الوساطة التقليدية",
    "Market Pedigree": "العراقة في السوق",
    "50+ Years (Yousuf Bin Nasser & Sons Foundation)": "أكثر من 50 عاماً (تأسيس يوسف بن ناصر وأولاده)",
    "Short-term agency with high agent turnover": "وكالة قصيرة الأمد مع دوران وظيفي مرتفع للوسطاء",
    "Facility & Building Maintenance": "صيانة المرافق والمباني",
    "In-House 24/7 Engineers + Audited Material Costs": "مهندسون وفنيون داخليون 24/7 + تكاليف مواد مدققة",
    "Outsourced third-party contractors with heavy markups": "مقاولون خارجيون مع هوامش ربح إضافية مرتفعة",
    "Financial & Cheque Tracking": "المتابعة المالية وإدارة الشيكات",
    "Automated Ledger Sync, PDC Alerts & Itemized Audits": "مزامنة محاسبية آلية، تنبيهات الشيكات، وتدقيق مفصل",
    "Manual spreadsheets and delayed owner statements": "جداول يدوية وتأخر في كشوفات حسابات الملاك",
    "Average Portfolio Occupancy": "متوسط إشغال المحفظة",
    "99.9% Across Managed Residential & Commercial Assets": "99.9% عبر الأصول السكنية والتجارية المدارة",
    "82% – 88% due to slow unit turnaround": "82% – 88% بسبب بطء تجهيز الوحدات وإعادة تأجيرها",
    "Alignment of Interest": "توافق المصالح",
    "Principal Asset Owners—We Manage What We Own": "ملاك أصول رئيسيون — ندير عقارك كما ندير ملكنا",
    "Commission-driven transaction focus only": "تركيز يقتصر على عمولة الصفقة فقط",
    "Live Backend Portfolio": "محفظة المباني الحية",
    "Buildings": "مبنى",
    "Our Landmark Buildings & Developments": "مبانينا ومشاريعنا العمرانية البارزة",
    "All Buildings": "جميع المباني",
    "Edrak Managed": "بإدارة إدراك",
    "Units": "وحدة",
    "Inspect Building": "استعراض المبنى",
    "Available Units": "الوحدات المتاحة",
    "No buildings have been added to the database yet. Add projects in the dashboard to display them here automatically.": "لم تتم إضافة مباني في قاعدة البيانات بعد. أضف المشاريع من لوحة التحكم لتظهر هنا تلقائياً.",
    "View Full Projects Directory": "عرض دليل المشاريع الكامل",
    "Immediate Residency & Commercial Spaces": "وحدات سكنية ومساحات تجارية جاهزة",
    "Active Listings": "وحدة نشطة",
    "Featured Units From Our Database": "وحدات مختارة من قاعدة بياناتنا",
    "Explore All Available Leases": "استكشف جميع الإيجارات المتاحة",
    "Year": "سنوياً",
    "Beds": "غرف",
    "Baths": "حمامات",
    "Sq.Ft": "قدم مربع",
    "View Unit Details": "عرض تفاصيل الوحدة",
    "Operational Architecture": "الهيكلية التشغيلية",
    "How We Protect Every Square Foot.": "كيف نحمي كل قدم مربع.",
    "Behind Edrak's calm luxury exterior sits a relentless operational machine. Every building in our care undergoes strict daily protocols designed to eliminate landlord headaches and maximize resident satisfaction.": "خلف الواجهة الفاخرة لشركة إدراك تعمل منظومة تشغيلية دقيقة لا تهدأ. يخضع كل مبنى تحت رعايتنا لبروتوكولات يومية صارمة مصممة لراحة بال الملاك وتحقيق أعلى درجات الرضا للسكان.",
    "Direct Headquarters Oversight": "إشراف مباشر من المقر الرئيسي",
    "Our doors at Rashidiya Building M5 are open daily. Landlords and tenants speak directly with decision-makers, engineers, and senior portfolio accountants—never an offshore call center.": "أبوابنا في بناية الراشدية M5 مفتوحة يومياً. يتحدث الملاك والمستأجرون مباشرة مع صناع القرار والمهندسين وكبار محاسبي المحافظ — وليس مع مراكز اتصال خارجية.",
    "Preventive Engineering & Audited Maintenance": "الهندسة الوقائية والصيانة المدققة",
    "Rather than waiting for expensive breakdowns, our technical teams execute scheduled seasonal servicing across all chillers, split AC units, lift rooms, water pumps, and waterproofing membranes. Every material invoice is cross-audited against historical supplier pricing so owners never overpay.": "بدلاً من انتظار الأعطال المكلفة، تنفذ فرقنا الفنية صيانة موسمية مجدولة لكافة أنظمة التبريد والتكييف والمصاعد ومضخات المياه والعزل. ويتم تدقيق كل فاتورة مواد مقارنة بالأسعار المرجعية للموردين لضمان عدم تحمل الملاك أي تكاليف زائدة.",
    "Zero-Leakage Rent Collection & Legal Custody": "تحصيل الإيجارات بالكامل والحماية القانونية",
    "Our leasing division manages the entire cheque lifecycle—from Tasdeeq contract registration and security deposit custody to automated pre-deposit notifications. If a payment exception ever arises, our in-house legal liaison handles municipal dispute resolution swiftly and compliantly.": "يدير قسم التأجير لدينا دورة حياة الشيكات بالكامل — بدءاً من تسجيل عقود تصديق وحفظ التأمينات وصولاً إلى الإشعارات الآلية قبل الإيداع. وفي حال حدوث أي استثناء في السداد، يتولى فريق المتابعة القانونية تسوية المنازعات البلدية بسرعة ووفق الأصول القانونية.",
    "Strategic Capital Appreciation & Refurbishment": "تنمية القيمة الرأسمالية والتجديد الاستراتيجي",
    "Older buildings in Ajman often suffer from rental stagnation. Edrak advises on and executes high-ROI modernizations—upgrading lobbies, lighting, kitchens, and sanitary fittings—allowing older family buildings to command premium modern rental rates.": "كثيراً ما تعاني المباني القديمة من ركود القيمة الإيجارية. تقدم إدراك استشارات وتنفذ عمليات تحديث عالية العائد — تشمل تطوير المداخل والإضاءة والمطابخ والتجهيزات الصحية — مما يتيح للمباني العائلية تحقيق عوائد إيجارية تنافس المباني الحديثة.",
    "Bespoke Advisory for Global & Institutional Buyers": "استشارات مخصصة للمشترين العالميين والمؤسسات",
    "For investors acquiring whole residential towers, industrial warehouses, or off-plan allocations, we provide unvarnished feasibility studies grounded in 50 years of real transaction data across Ajman and the UAE.": "للمستثمرين الراغبين في الاستحواذ على أبراج سكنية كاملة أو مستودعات صناعية أو حصص على الخارطة، نقدم دراسات جدوى دقيقة تستند إلى 50 عاماً من بيانات الصفقات الفعلية في عجمان والإمارات.",
    "Enduring Relationships": "علاقات راسخة عبر السنين",
    "Trusted by Landlords, Investors & Families": "محل ثقة الملاك والمستثمرين والعائلات",
    "Our family has entrusted our Ajman residential buildings to Yousuf Bin Nasser & Sons—and now Edrak Properties—for over two decades. Under Mr. Mohammed Al Nuaimi's leadership, our occupancy has remained near 100% and our maintenance costs are the most transparent in the Emirates.": "عهدت عائلتنا بإدارة مبانينا السكنية في عجمان إلى شركة يوسف بن ناصر وأولاده — والآن إدراك العقارية — لأكثر من عقدين من الزمن. وتحت قيادة السيد محمد النعيمي، ظلت نسبة الإشغال لدينا قريبة من 100% وتكاليف الصيانة هي الأكثر شفافية في الإمارات.",
    "Private Multi-Tower Landlord": "مالك خاص لعدة أبراج سكنية",
    "22-Year Portfolio Client • Ajman & Dubai": "عميل محفظة منذ 22 عاماً • عجمان ودبي",
    "As an overseas investor, I needed a partner who actually owns buildings and understands facility engineering, not a flashy sales broker. Edrak sourced our commercial asset, vetted every corporate tenant, and deposits our net yield like clockwork.": "كمستثمر مقيم في الخارج، كنت بحاجة إلى شريك يمتلك المباني فعلياً ويفهم هندسة المرافق، وليس مجرد وسيط مبيعات. وفرت لنا إدراك الأصل التجاري، وفحصت كل مستأجر بدقة، وتودع صافي عوائدنا في موعدها المحدد دائماً.",
    "GCC Institutional Investor": "مستثمر مؤسسي خليجي",
    "Commercial & Industrial Portfolio": "محفظة عقارية تجارية وصناعية",
    "Living in an Edrak-managed building feels completely different from other properties in the city. The security staff know every family, the corridors are spotless, and if an AC ever needs servicing, their technical team arrives the same day.": "السكن في مبنى تديره شركة إدراك يختلف تماماً عن أي عقار آخر في المدينة. موظفو الأمن يعرفون كل عائلة، والممرات نظيفة دائماً، وإذا احتاج التكييف لأي صيانة فإن فريقهم الفني يصل في نفس اليوم.",
    "Long-Term Resident Family": "عائلة مقيمة منذ سنوات طويلة",
    "8-Year Tenant • Rashidiya, Ajman": "مستأجر منذ 8 سنوات • الراشدية، عجمان",
    "Yousuf Bin Nasser & Sons Pedigree • Edrak Future": "عراقة يوسف بن ناصر وأولاده • مستقبل إدراك",
    "Place Your Assets in Half-Century Hands.": "ضع أصولك العقارية في أيدٍ أمينة تمتد لنصف قرن.",
    "Whether you are looking to assign a residential tower for turnkey management, acquire high-yield UAE real estate, or lease a premier residence or commercial space, our executive team is ready to welcome you.": "سواء كنت تتطلع إلى إسناد إدارة برج سكني بالكامل، أو الاستحواذ على عقارات عالية العائد في الإمارات، أو استئجار مسكن متميز أو مساحة تجارية، فإن فريقنا التنفيذي مستعد للترحيب بك.",
    "Schedule an Executive Consultation": "احجز استشارة تنفيذية",
    "Explore All Buildings": "استكشف جميع المباني",
}


def generate_po_and_mo():
    locale_dir = os.path.join("locale", "ar", "LC_MESSAGES")
    os.makedirs(locale_dir, exist_ok=True)
    po_path = os.path.join(locale_dir, "django.po")
    mo_path = os.path.join(locale_dir, "django.mo")

    # 1. Write django.po
    with open(po_path, "w", encoding="utf-8") as f:
        f.write('msgid ""\n')
        f.write('msgstr ""\n')
        f.write('"Project-Id-Version: Edrak Properties\\n"\n')
        f.write('"Language: ar\\n"\n')
        f.write('"MIME-Version: 1.0\\n"\n')
        f.write('"Content-Type: text/plain; charset=UTF-8\\n"\n')
        f.write('"Content-Transfer-Encoding: 8bit\\n"\n')
        f.write('"Plural-Forms: nplurals=6; plural=n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : n%100>=11 && n%100<=99 ? 4 : 5;\\n"\n\n')

        for msgid, msgstr in TRANSLATIONS.items():
            esc_id = msgid.replace('\\', '\\\\').replace('"', '\\"')
            esc_str = msgstr.replace('\\', '\\\\').replace('"', '\\"')
            f.write(f'msgid "{esc_id}"\n')
            f.write(f'msgstr "{esc_str}"\n\n')

    # 2. Compile binary django.mo in pure Python (no external gettext required)
    messages = {
        "": (
            "Project-Id-Version: Edrak Properties\n"
            "Language: ar\n"
            "MIME-Version: 1.0\n"
            "Content-Type: text/plain; charset=UTF-8\n"
            "Content-Transfer-Encoding: 8bit\n"
            "Plural-Forms: nplurals=6; plural=n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : n%100>=11 && n%100<=99 ? 4 : 5;\n"
        )
    }
    messages.update(TRANSLATIONS)

    keys = sorted(messages.keys())
    offsets = []
    ids = b""
    strs = b""

    for k in keys:
        b_id = k.encode("utf-8")
        b_str = messages[k].encode("utf-8")
        offsets.append((len(ids), len(b_id), len(strs), len(b_str)))
        ids += b_id + b"\x00"
        strs += b_str + b"\x00"

    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + len(ids)
    koffsets = []
    voffsets = []

    for o1, l1, o2, l2 in offsets:
        koffsets += [l1, o1 + keystart]
        voffsets += [l2, o2 + valuestart]

    output = struct.pack(
        "Iiiiiii",
        0x950412DE,       # Magic number
        0,                # Version
        len(keys),        # # of entries
        7 * 4,            # Start of key index
        7 * 4 + len(keys) * 8,  # Start of value index
        0, 0              # Size and offset of hash table
    )
    output += array.array("i", koffsets).tobytes()
    output += array.array("i", voffsets).tobytes()
    output += ids
    output += strs

    with open(mo_path, "wb") as f:
        f.write(output)

    print(f"Successfully generated {po_path} and compiled {mo_path} ({len(TRANSLATIONS)} Arabic translations)!")


if __name__ == "__main__":
    generate_po_and_mo()