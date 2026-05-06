import React, { useState } from 'react';
import axios from 'axios';
import { Activity, Brain, Zap, FlaskConical, TrendingUp, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const FeatureInput = ({ label, name, value, onChange, type = "number", step = "0.1" }) => (
  <div className="flex flex-col mb-4">
    <label className="text-sm font-semibold text-slate-600 mb-1">{label}</label>
    <input
      type={type}
      name={name}
      value={value}
      onChange={onChange}
      step={step}
      className="px-4 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all"
      required
    />
  </div>
);

const PredictionCard = ({ title, data, icon: Icon, color }) => {
  if (!data || typeof data === 'string') return null;
  
  const isHighRisk = data.label === "High Risk";
  
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white p-6 rounded-2xl shadow-sm border border-slate-100 flex flex-col"
    >
      <div className="flex items-center gap-3 mb-4">
        <div className={`p-2 rounded-lg ${color}`}>
          <Icon className="w-5 h-5 text-white" />
        </div>
        <h3 className="font-bold text-slate-800">{title}</h3>
      </div>
      <div className="flex-1">
        <div className="text-3xl font-black text-slate-900 mb-1">
          {(data.risk_score * 100).toFixed(1)}%
        </div>
        <div className={`text-sm font-bold flex items-center gap-1 ${isHighRisk ? 'text-rose-500' : 'text-emerald-500'}`}>
          {isHighRisk ? <ShieldAlert className="w-4 h-4" /> : <CheckCircle2 className="w-4 h-4" />}
          {data.label}
        </div>
      </div>
    </motion.div>
  );
};

export default function App() {
  const [formData, setFormData] = useState({
    age: 45, bmi: 28.5, glucose: 110, blood_pressure: 130,
    cholesterol: 210, heart_rate: 75, insulin: 50,
    smoking: 0, physical_activity: 3, sleep_hours: 7
  });

  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleChange = (e) => {
    const value = e.target.type === 'number' ? parseFloat(e.target.value) : parseInt(e.target.value);
    setFormData({ ...formData, [e.target.name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/analyze', formData);
      setResults(response.data);
    } catch (error) {
      console.error("API Error:", error);
      alert("Failed to fetch predictions. Ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 p-4 md:p-8">
      {/* Docker Verification Banner */}
      <div className="max-w-6xl mx-auto mb-4">
        <div className="bg-blue-600 text-white p-3 text-center rounded-2xl font-black shadow-xl animate-pulse">
          🚀 DOCKER STATUS: HELLO WORLD! (Platform is Running in Containers)
        </div>
      </div>

      <div className="max-w-6xl mx-auto">
        <header className="mb-10 text-center">
          <div className="inline-flex items-center gap-2 bg-emerald-100 text-emerald-700 px-4 py-1.5 rounded-full text-sm font-bold mb-4">
            <Activity className="w-4 h-4" />
            AI Diagnostics
          </div>
          <h1 className="text-4xl md:text-5xl font-black text-slate-900 mb-2">Unified Health AI</h1>
          <p className="text-slate-500 max-w-2xl mx-auto">
            Standardized health risk assessment using Ensemble Machine Learning, 
            Attention-based Deep Learning, and Variational Quantum Circuits.
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Form Section */}
          <div className="lg:col-span-4">
            <div className="bg-white p-8 rounded-3xl shadow-xl shadow-slate-200/50 border border-slate-100">
              <h2 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
                <FlaskConical className="w-5 h-5 text-emerald-500" />
                Patient Vitals
              </h2>
              <form onSubmit={handleSubmit}>
                <div className="grid grid-cols-2 gap-4">
                  <FeatureInput label="Age" name="age" value={formData.age} onChange={handleChange} />
                  <FeatureInput label="BMI" name="bmi" value={formData.bmi} onChange={handleChange} />
                </div>
                <FeatureInput label="Glucose" name="glucose" value={formData.glucose} onChange={handleChange} />
                <FeatureInput label="Blood Pressure" name="blood_pressure" value={formData.blood_pressure} onChange={handleChange} />
                <FeatureInput label="Cholesterol" name="cholesterol" value={formData.cholesterol} onChange={handleChange} />
                <div className="grid grid-cols-2 gap-4">
                  <FeatureInput label="Heart Rate" name="heart_rate" value={formData.heart_rate} onChange={handleChange} />
                  <FeatureInput label="Insulin" name="insulin" value={formData.insulin} onChange={handleChange} />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <FeatureInput label="Smoking (0/1)" name="smoking" value={formData.smoking} onChange={handleChange} type="number" step="1" />
                  <FeatureInput label="Activity (0-7)" name="physical_activity" value={formData.physical_activity} onChange={handleChange} step="1" />
                </div>
                <FeatureInput label="Sleep Hours" name="sleep_hours" value={formData.sleep_hours} onChange={handleChange} />
                
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-slate-900 text-white font-bold py-4 rounded-xl mt-4 hover:bg-slate-800 transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  {loading ? (
                    <div className="w-6 h-6 border-4 border-white/20 border-t-white rounded-full animate-spin" />
                  ) : (
                    <>Run Unified Analysis</>
                  )}
                </button>
              </form>
            </div>
          </div>

          {/* Results Section */}
          <div className="lg:col-span-8">
            <AnimatePresence mode="wait">
              {results ? (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="space-y-6"
                >
                  {/* Consensus Banner */}
                  <div className={`p-6 rounded-3xl flex items-center justify-between border ${results.comparison.consensus === 'High Risk' ? 'bg-rose-50 border-rose-100 text-rose-900' : 'bg-emerald-50 border-emerald-100 text-emerald-900'}`}>
                    <div>
                      <h3 className="text-sm uppercase tracking-wider font-black opacity-60">Consensus Result</h3>
                      <div className="text-3xl font-black">{results.comparison.consensus}</div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-bold opacity-60">Average Risk Score</div>
                      <div className="text-3xl font-black">{(results.comparison.average_risk * 100).toFixed(1)}%</div>
                    </div>
                  </div>

                  {/* Individual Models */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <PredictionCard title="ML Ensemble" data={results.ml_prediction} icon={Brain} color="bg-blue-500" />
                    <PredictionCard title="Deep Attention" data={results.dl_prediction} icon={Zap} color="bg-amber-500" />
                    <PredictionCard title="Quantum ML" data={results.qml_prediction} icon={Activity} color="bg-indigo-500" />
                  </div>

                  {/* Comparison Table */}
                  <div className="bg-white rounded-3xl p-8 shadow-sm border border-slate-100">
                    <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                      <TrendingUp className="w-5 h-5 text-emerald-500" />
                      Platform Comparison
                    </h3>
                    <div className="overflow-x-auto">
                      <table className="w-full text-left">
                        <thead>
                          <tr className="border-b border-slate-100">
                            <th className="pb-4 font-bold text-slate-500 text-sm">Model Paradigm</th>
                            <th className="pb-4 font-bold text-slate-500 text-sm">Risk Score</th>
                            <th className="pb-4 font-bold text-slate-500 text-sm">Status</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-50">
                          {['ml_prediction', 'dl_prediction', 'qml_prediction'].map((key) => (
                            <tr key={key}>
                              <td className="py-4 font-semibold text-slate-700 capitalize">{key.split('_')[0].toUpperCase()}</td>
                              <td className="py-4 text-slate-900 font-bold">
                                {typeof results[key] === 'object' ? `${(results[key].risk_score * 100).toFixed(1)}%` : 'N/A'}
                              </td>
                              <td className="py-4">
                                <span className={`px-3 py-1 rounded-full text-xs font-black uppercase ${results[key]?.label === 'High Risk' ? 'bg-rose-100 text-rose-600' : 'bg-emerald-100 text-emerald-600'}`}>
                                  {results[key]?.label || 'Error'}
                                </span>
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </motion.div>
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-center p-12 bg-white rounded-3xl border-2 border-dashed border-slate-200">
                  <div className="bg-slate-100 p-4 rounded-full mb-4">
                    <FlaskConical className="w-12 h-12 text-slate-400" />
                  </div>
                  <h3 className="text-xl font-bold text-slate-800">Ready for Analysis</h3>
                  <p className="text-slate-500 max-w-xs">Enter patient features on the left and run the diagnostic pipeline to see AI comparisons.</p>
                </div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
}
