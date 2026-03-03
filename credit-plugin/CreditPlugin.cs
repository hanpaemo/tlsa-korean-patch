using BepInEx;
using BepInEx.Unity.IL2CPP;
using UnityEngine;

namespace HanpaemoCredit;

[BepInPlugin("hanpaemo.credit", "KOR by 한패모", "1.0.0")]
public class CreditPlugin : BasePlugin
{
    public override void Load()
    {
        AddComponent<CreditBehaviour>();
    }
}

public class CreditBehaviour : MonoBehaviour
{
    public CreditBehaviour(System.IntPtr ptr) : base(ptr) { }

    private GUIStyle? _style;
    private const string Text = "KOR by 한패모";

    private void OnGUI()
    {
        if (_style == null)
        {
            // Malgun Gothic is pre-installed on Windows and supports Korean
            var font = Font.CreateDynamicFontFromOSFont(
                new[] { "Malgun Gothic", "NanumGothic", "Arial" }, 12);
            _style = new GUIStyle(GUI.skin.label)
            {
                fontSize = 12,
                alignment = TextAnchor.UpperRight,
                font = font,
            };
            _style.normal.textColor = new Color(1f, 1f, 1f, 0.40f);
        }

        var w = Screen.width;
        var h = Screen.height;
        GUI.Label(new Rect(w - 160, h - 30, 150, 22), Text, _style);
    }
}
