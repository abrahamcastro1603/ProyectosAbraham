
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cuestionario Metodología CRISP-DM</title>
    <style>
        :root {
            --primary-color: #2563eb;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-color: #1e293b;
            --border-color: #e2e8f0;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: var(--card-bg);
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }

        h1 {
            color: var(--primary-color);
            text-align: center;
            margin-bottom: 10px;
        }

        .description {
            text-align: center;
            color: #64748b;
            margin-bottom: 40px;
        }

        .phase-section {
            margin-bottom: 35px;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 20px;
        }

        .phase-section:last-child {
            border-bottom: none;
        }

        .phase-title {
            font-size: 1.3rem;
            color: var(--primary-color);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .question-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            font-weight: 500;
            margin-bottom: 8px;
        }

        textarea {
            width: 100%;
            min-height: 80px;
            padding: 12px;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            resize: vertical;
            font-family: inherit;
            box-sizing: border-box;
            transition: border-color 0.2s;
        }

        textarea:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }

        .btn-submit {
            display: block;
            width: 100%;
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 14px;
            font-size: 1rem;
            font-weight: 600;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        .btn-submit:hover {
            background-color: #1d4ed8;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>Guía de Cuestionario CRISP-DM</h1>
    <p class="description">Responde a las siguientes preguntas clave para estructurar correctamente tu proyecto de Minería de Datos.</p>

    <form id="crispForm" onsubmit="handleSubmit(event)">
        
        <!-- Fase 1 -->
        <div class="phase-section">
            <div class="phase-title">1. Comprensión del Negocio (Business Understanding)</div>
            
            <div class="question-group">
                <label for="b1">¿Cuál es el objetivo principal de la organización o negocio?</label>
                <textarea id="b1" name="business_obj" placeholder="Ej. Incrementar las ventas, reducir la fuga de clientes..."></textarea>
            </div>
            <div class="question-group">
                <label for="b2">¿Qué problema específico se necesita resolver o qué oportunidad se quiere aprovechar?</label>
                <textarea id="b2" name="business_prob"></textarea>
            </div>
            <div class="question-group">
                <label for="b3">¿Cómo se traducen las necesidades del negocio en preguntas orientadas a la minería de datos?</label>
                <textarea id="b3" name="business_dm_trans"></textarea>
            </div>
            <div class="question-group">
                <label for="b4">¿Cuáles son los criterios de éxito del proyecto desde la perspectiva del negocio?</label>
                <textarea id="b4" name="business_success"></textarea>
            </div>
        </div>

        <!-- Fase 2 -->
        <div class="phase-section">
            <div class="phase-title">2. Comprensión de los Datos (Data Understanding)</div>
            
            <div class="question-group">
                <label for="d1">¿Qué datos están disponibles y dónde se encuentran almacenados?</label>
                <textarea id="d1" name="data_avail"></textarea>
            </div>
            <div class="question-group">
                <label for="d2">¿Cuántas fuentes de datos se van a utilizar y qué formatos tienen?</label>
                <textarea id="d2" name="data_sources"></textarea>
            </div>
            <div class="question-group">
                <label for="d3">¿Cuál es la calidad inicial de los datos y existen valores perdidos o sesgos?</label>
                <textarea id="d3" name="data_quality"></textarea>
            </div>
            <div class="question-group">
                <label for="d4">¿Qué patrones preliminares o inconsistencias se observan al explorar los datos?</label>
                <textarea id="d4" name="data_explor"></textarea>
            </div>
        </div>

        <!-- Fase 3 -->
        <div class="phase-section">
            <div class="phase-title">3. Preparación de los Datos (Data Preparation)</div>
            
            <div class="question-group">
                <label for="p1">¿Cómo se deben tratar los valores nulos, atípicos o duplicados?</label>
                <textarea id="p1" name="prep_cleaning"></textarea>
            </div>
            <div class="question-group">
                <label for="p2">¿Los atributos y variables están en el formato correcto para el análisis?</label>
                <textarea id="p2" name="prep_format"></textarea>
            </div>
            <div class="question-group">
                <label for="p3">¿Es necesario integrar o fusionar múltiples tablas o fuentes de datos?</label>
                <textarea id="p3" name="prep_integration"></textarea>
            </div>
            <div class="question-group">
                <label for="p4">¿Qué variables nuevas o transformaciones se requieren para mejorar el modelo?</label>
                <textarea id="p4" name="prep_eng"></textarea>
            </div>
        </div>

        <!-- Fase 4 -->
        <div class="phase-section">
            <div class="phase-title">4. Modelado (Modeling)</div>
            
            <div class="question-group">
                <label for="m1">¿Qué técnicas o algoritmos de machine learning son los más adecuados?</label>
                <textarea id="m1" name="model_tech"></textarea>
            </div>
            <div class="question-group">
                <label for="m2">¿Cómo se dividirá el conjunto de datos para el entrenamiento y la prueba del modelo?</label>
                <textarea id="m2" name="model_split"></textarea>
            </div>
            <div class="question-group">
                <label for="m3">¿Qué parámetros del modelo se pueden ajustar para optimizar su rendimiento?</label>
                <textarea id="m3" name="model_hyper"></textarea>
            </div>
            <div class="question-group">
                <label for="m4">¿El modelo responde de manera técnica al objetivo planteado?</label>
                <textarea id="m4" name="model_eval_tech"></textarea>
            </div>
        </div>

        <!-- Fase 5 -->
        <div class="phase-section">
            <div class="phase-title">5. Evaluación (Evaluation)</div>
            
            <div class="question-group">
                <label for="e1">¿El modelo cumple con los criterios de éxito establecidos en la fase de negocio?</label>
                <textarea id="e1" name="eval_business"></textarea>
            </div>
            <div class="question-group">
                <label for="e2">¿Los resultados son confiables y operativos en un entorno real?</label>
                <textarea id="e2" name="eval_reliability"></textarea>
            </div>
            <div class="question-group">
                <label for="e3">¿Cuáles son los costos asociados a los posibles errores de predicción?</label>
                <textarea id="e3" name="eval_costs"></textarea>
            </div>
            <div class="question-group">
                <label for="e4">¿Se debe aprobar el paso a producción o es necesario regresar a fases anteriores?</label>
                <textarea id="e4" name="eval_decision"></textarea>
            </div>
        </div>

        <!-- Fase 6 -->
        <div class="phase-section">
            <div class="phase-title">6. Despliegue (Deployment)</div>
            
            <div class="question-group">
                <label for="dp1">¿Cómo se integrará el modelo en los sistemas o procesos diarios?</label>
                <textarea id="dp1" name="deploy_integration"></textarea>
            </div>
            <div class="question-group">
                <label for="dp2">¿Quién será el encargado de utilizar los resultados e interpretar las decisiones?</label>
                <textarea id="dp2" name="deploy_users"></textarea>
            </div>
            <div class="question-group">
                <label for="dp3">¿Cómo se realizará el mantenimiento y monitoreo continuo ante cambios en los datos?</label>
                <textarea id="dp3" name="deploy_monitor"></textarea>
            </div>
        </div>

        <button type="submit" class="btn-submit">Guardar Cuestionario</button>
    </form>
</div>

<script>
    function handleSubmit(event) {
        event.preventDefault();
