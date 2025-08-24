import React, { useState, useEffect } from "react";
import { uploadFile, listFiles, deleteFile } from "../lib/api/s3";

const S3Manager: React.FC = () => {
  const [files, setFiles] = useState<string[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const fetchFiles = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await listFiles();
      setFiles(data);
    } catch (e: any) {
      setError(e.message);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      await uploadFile(selectedFile);
      setSuccess("Archivo subido correctamente");
      setSelectedFile(null);
      fetchFiles();
    } catch (e: any) {
      setError(e.message);
    }
    setLoading(false);
  };

  const handleDelete = async (filename: string) => {
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      await deleteFile(filename);
      setSuccess("Archivo borrado correctamente");
      fetchFiles();
    } catch (e: any) {
      setError(e.message);
    }
    setLoading(false);
  };

  return (
    <div className="max-w-xl mx-auto p-4">
      <h2 className="text-xl font-bold mb-4">Gestión de Archivos S3</h2>
      <div className="mb-4">
        <input type="file" onChange={handleFileChange} />
        <button
          className="ml-2 px-4 py-2 bg-blue-600 text-white rounded"
          onClick={handleUpload}
          disabled={!selectedFile || loading}
        >
          Subir
        </button>
      </div>
      {success && <div className="text-green-600 mb-2">{success}</div>}
      {error && <div className="text-red-600 mb-2">{error}</div>}
      <h3 className="font-semibold mb-2">Historial de archivos:</h3>
      {loading ? (
        <div>Cargando...</div>
      ) : (
        <ul className="divide-y divide-gray-200">
          {files.map((file) => (
            <li key={file} className="flex items-center justify-between py-2">
              <span>{file}</span>
              <button
                className="ml-4 px-2 py-1 bg-red-500 text-white rounded"
                onClick={() => handleDelete(file)}
                disabled={loading}
              >
                Borrar
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default S3Manager;
