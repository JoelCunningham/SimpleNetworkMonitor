import { LastScanText } from '#components/fields';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('LastScanText', () => {
  let component: LastScanText;
  let fixture: ComponentFixture<LastScanText>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LastScanText],
    }).compileComponents();

    fixture = TestBed.createComponent(LastScanText);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
